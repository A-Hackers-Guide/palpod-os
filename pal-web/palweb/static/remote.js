// pal-web remote UI client.
//
// Security notes worth reading before you edit this file:
//   * The Grant modal's confirm handler is the ONLY code path that sends
//     `X-Consent-Origin: user-tap`. It runs synchronously inside the click
//     handler of the physical "Grant control" button. No other code path
//     — voice, websocket message, or timer — sets that header.
//   * The canvas captures mouse/keyboard events only when the user has
//     TICKED the "Send my input" checkbox. Ticking is not persisted across
//     reloads.
//   * The server enforces the grant window on every event. This UI is
//     convenience — not the security boundary.

(() => {
  const state = {
    devices: [],
    activeDevice: null,       // device object currently in the viewer
    activeSession: null,      // session id string currently open
    ws: null,
    sendInput: false,
    grantExpiresAt: null,     // Date | null
    countdownTimer: null,
    grantModalDeviceId: null,
  };

  const $ = (sel) => document.querySelector(sel);
  const el = (tag, attrs = {}, ...kids) => {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") node.className = v;
      else if (k.startsWith("on") && typeof v === "function") node.addEventListener(k.slice(2), v);
      else if (v !== null && v !== undefined) node.setAttribute(k, v);
    }
    for (const kid of kids) {
      if (kid == null) continue;
      node.appendChild(typeof kid === "string" ? document.createTextNode(kid) : kid);
    }
    return node;
  };

  // ------------------------------------------------------------------- //
  // API helpers
  // ------------------------------------------------------------------- //

  // Read the CSRF token seated by the server. Single source of truth:
  //   <meta name="csrf-token"> — stamped in by the /remote.html handler
  //   from the seeded palpod_csrf cookie value.
  //
  // The previous dual read path (meta + document.cookie fallback) is gone.
  // A same-origin XSS could always read document.cookie and echo it, but
  // the router-level `require_csrf_double_submit` dependency + the CSPMiddleware
  // + the move of remote.html out of the static tree close the door with
  // real defenses; not with a JS trick. Reading from ONE place keeps the
  // client simple and impossible to get out of sync with the seeded value.
  function readCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta && meta.getAttribute("content") ? meta.getAttribute("content") : "";
  }

  async function apiJSON(url, opts = {}) {
    const method = (opts.method || "GET").toUpperCase();
    const extraHeaders = { "Content-Type": "application/json", ...(opts.headers || {}) };
    // Every state-changing call MUST double-submit the CSRF token. Adding it
    // to GETs too is harmless (server ignores it) and simplifies the code.
    const csrf = readCsrfToken();
    if (csrf) extraHeaders["X-CSRF-Token"] = csrf;

    const res = await fetch(url, {
      ...opts,
      credentials: "same-origin",
      headers: extraHeaders,
    });
    if (!res.ok) {
      let detail = res.statusText;
      try { detail = (await res.json()).detail || detail; } catch (_) {}
      throw new Error(`${res.status}: ${detail}`);
    }
    if (res.status === 204) return null;
    return res.json();
  }

  async function refreshDevices() {
    state.devices = await apiJSON("/api/remote/devices");
    renderDeviceList();
    // The audit trail follows the device list so it's always in sync.
    await refreshAuditTrail().catch(() => {});
  }

  async function refreshAuditTrail() {
    const container = $("#audit-trail");
    if (!container) return;
    container.innerHTML = "";
    if (state.devices.length === 0) {
      container.appendChild(el("p", { class: "pal-subtle" }, "No devices yet."));
      return;
    }
    for (const d of state.devices) {
      let events = [];
      try {
        events = await apiJSON(`/api/remote/devices/${d.id}/grant-events`);
      } catch (_) {
        events = [];
      }
      const group = el("div", { class: "pal-audit-device" },
        el("h3", { class: "pal-audit-device-title" }, d.display_name),
      );
      if (events.length === 0) {
        group.appendChild(el("p", { class: "pal-subtle pal-small" }, "No grants yet."));
      } else {
        const list = el("ul", { class: "pal-audit-list" });
        for (const ev of events) {
          const at = new Date(ev.granted_at).toLocaleString();
          const label = ev.revoked_early_at
            ? `granted ${ev.minutes} min at ${at}, revoked ${new Date(ev.revoked_early_at).toLocaleTimeString()}`
            : `granted ${ev.minutes} min at ${at} — origin ${ev.origin}`;
          list.appendChild(el("li", { class: "pal-audit-row" }, label));
        }
        group.appendChild(list);
      }
      container.appendChild(group);
    }
  }

  // ------------------------------------------------------------------- //
  // Rendering
  // ------------------------------------------------------------------- //

  function renderDeviceList() {
    const list = $("#device-list");
    list.innerHTML = "";
    if (state.devices.length === 0) {
      list.appendChild(el("p", { class: "pal-subtle" }, "No devices paired yet."));
      return;
    }
    for (const d of state.devices) list.appendChild(renderDeviceRow(d));
  }

  function renderDeviceRow(device) {
    const stateLabel = device.control_state === "granted"
      ? `granted until ${new Date(device.control_grant_expires_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`
      : "view-only";

    const stateBadge = el(
      "span",
      { class: `pal-badge pal-badge-${device.control_state}` },
      stateLabel
    );

    const actions = el("div", { class: "pal-device-actions" },
      el("button", {
        class: "pal-btn",
        onclick: () => openViewer(device),
      }, "View live"),
      el("button", {
        class: "pal-btn",
        onclick: () => openGrantModal(device),
      }, "Grant control"),
      device.control_state === "granted"
        ? el("button", {
            class: "pal-btn pal-btn-danger",
            onclick: () => revokeControl(device),
          }, "Revoke control")
        : null,
      el("button", {
        class: "pal-btn pal-btn-danger",
        onclick: () => unpairDevice(device),
      }, "Unpair"),
    );

    return el("div", { class: "pal-device-row", "data-device-id": device.id },
      el("div", { class: "pal-device-info" },
        el("div", { class: "pal-device-name" }, device.display_name),
        el("div", { class: "pal-subtle pal-small" }, `${device.device_type} · ${device.rustdesk_id}`),
      ),
      stateBadge,
      actions,
    );
  }

  // ------------------------------------------------------------------- //
  // Pairing
  // ------------------------------------------------------------------- //

  $("#pair-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
    try {
      await apiJSON("/api/remote/devices", { method: "POST", body: JSON.stringify(data) });
      e.target.reset();
      await refreshDevices();
    } catch (err) {
      alert(`Could not pair: ${err.message}`);
    }
  });

  async function unpairDevice(device) {
    if (!confirm(`Unpair ${device.display_name}?`)) return;
    await apiJSON(`/api/remote/devices/${device.id}`, { method: "DELETE" });
    await refreshDevices();
  }

  // ------------------------------------------------------------------- //
  // Grant modal — the single point where the user-tap header is set
  // ------------------------------------------------------------------- //

  function openGrantModal(device) {
    state.grantModalDeviceId = device.id;
    $("#grant-modal-device").textContent = device.display_name;
    $("#grant-modal").classList.remove("pal-hidden");
  }

  function closeGrantModal() {
    state.grantModalDeviceId = null;
    $("#grant-modal").classList.add("pal-hidden");
  }

  $("#grant-cancel").addEventListener("click", closeGrantModal);

  $("#grant-confirm").addEventListener("click", async () => {
    const deviceId = state.grantModalDeviceId;
    if (!deviceId) return;
    const picked = document.querySelector('input[name="grant-minutes"]:checked');
    const minutes = parseInt(picked ? picked.value : "15", 10);

    try {
      const result = await apiJSON(
        `/api/remote/devices/${deviceId}/grant-control`,
        {
          method: "POST",
          // THE consent gate. Set here and nowhere else in this codebase.
          headers: { "X-Consent-Origin": "user-tap" },
          body: JSON.stringify({ minutes }),
        }
      );
      closeGrantModal();
      await refreshDevices();
      if (state.activeDevice && state.activeDevice.id === deviceId) {
        state.grantExpiresAt = new Date(result.control_grant_expires_at);
        startCountdown();
      }
    } catch (err) {
      alert(`Could not grant control: ${err.message}`);
    }
  });

  async function revokeControl(device) {
    if (!confirm(`Revoke Pod's control of ${device.display_name}?`)) return;
    await apiJSON(`/api/remote/devices/${device.id}/revoke-control`, { method: "POST" });
    if (state.activeDevice && state.activeDevice.id === device.id) {
      state.grantExpiresAt = null;
      stopCountdown();
    }
    await refreshDevices();
  }

  // ------------------------------------------------------------------- //
  // Viewer
  // ------------------------------------------------------------------- //

  async function openViewer(device) {
    if (state.ws) closeViewer();

    const session = await apiJSON("/api/remote/sessions", {
      method: "POST",
      body: JSON.stringify({ device_id: device.id, initiated_by: "web" }),
    });

    state.activeDevice = device;
    state.activeSession = session.id;
    state.grantExpiresAt = device.control_grant_expires_at
      ? new Date(device.control_grant_expires_at)
      : null;

    $("#viewer-device-name").textContent = device.display_name;
    $("#viewer").classList.remove("pal-hidden");
    if (state.grantExpiresAt && state.grantExpiresAt > new Date()) startCountdown();

    const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
    state.ws = new WebSocket(`${proto}//${window.location.host}/ws/remote/${session.id}`);
    state.ws.addEventListener("message", onWsMessage);
    state.ws.addEventListener("close", () => { state.ws = null; });
  }

  function closeViewer() {
    if (state.ws) { try { state.ws.close(); } catch (_) {} state.ws = null; }
    state.activeDevice = null;
    state.activeSession = null;
    state.sendInput = false;
    $("#send-input-toggle").checked = false;
    $("#viewer").classList.add("pal-hidden");
    stopCountdown();
  }

  $("#close-viewer").addEventListener("click", closeViewer);

  function onWsMessage(ev) {
    let msg;
    try { msg = JSON.parse(ev.data); } catch (_) { return; }
    switch (msg.type) {
      case "frame":
        // Placeholder — the frame envelope carries metadata; a real
        // implementation would render msg.png_b64 into the canvas.
        break;
      case "grant_expired":
        state.grantExpiresAt = null;
        stopCountdown();
        refreshDevices();
        alert("The Pod's control window has ended. Grant again to continue.");
        break;
      case "error":
        console.warn("pal-web ws error:", msg);
        if (msg.code === 403) {
          // Server refused an input event. The UI should reflect the fact
          // that we're back to view-only.
          state.grantExpiresAt = null;
          stopCountdown();
          refreshDevices();
        }
        break;
    }
  }

  // ------------------------------------------------------------------- //
  // Input capture — off by default
  // ------------------------------------------------------------------- //

  $("#send-input-toggle").addEventListener("change", (e) => {
    state.sendInput = e.target.checked;
  });

  const canvas = $("#viewer-canvas");

  canvas.addEventListener("mousemove", (e) => forwardInput("mouse_move", canvasCoords(e)));
  canvas.addEventListener("click", (e) => forwardInput("mouse_click", { ...canvasCoords(e), button: e.button }));
  canvas.addEventListener("keydown", (e) => forwardInput("key_press", { key: e.key, modifiers: modifiersFor(e) }));

  function canvasCoords(e) {
    const rect = canvas.getBoundingClientRect();
    return { x: Math.round(e.clientX - rect.left), y: Math.round(e.clientY - rect.top) };
  }

  function modifiersFor(e) {
    const mods = [];
    if (e.ctrlKey) mods.push("ctrl");
    if (e.metaKey) mods.push("meta");
    if (e.altKey) mods.push("alt");
    if (e.shiftKey) mods.push("shift");
    return mods;
  }

  function forwardInput(event_type, payload) {
    if (!state.sendInput) return;
    if (!state.ws || state.ws.readyState !== WebSocket.OPEN) return;
    // Note: no `initiator` field is sent. The server derives it from the
    // authenticated principal at WS accept time — BYPASS #9 fix. Sending it
    // here is not merely ignored; the pydantic model refuses unknown fields.
    state.ws.send(JSON.stringify({ type: "input", event_type, payload }));
  }

  // ------------------------------------------------------------------- //
  // Countdown timer
  // ------------------------------------------------------------------- //

  function startCountdown() {
    stopCountdown();
    const badge = $("#grant-countdown");
    badge.classList.remove("pal-hidden");
    const tick = () => {
      if (!state.grantExpiresAt) { stopCountdown(); return; }
      const remaining = Math.max(0, state.grantExpiresAt.getTime() - Date.now());
      if (remaining <= 0) { stopCountdown(); refreshDevices(); return; }
      const m = Math.floor(remaining / 60000);
      const s = Math.floor((remaining % 60000) / 1000);
      badge.textContent = `Control expires in ${m}:${String(s).padStart(2, "0")}`;
    };
    tick();
    state.countdownTimer = setInterval(tick, 500);
  }

  function stopCountdown() {
    if (state.countdownTimer) { clearInterval(state.countdownTimer); state.countdownTimer = null; }
    const badge = $("#grant-countdown");
    if (badge) badge.classList.add("pal-hidden");
  }

  // ------------------------------------------------------------------- //
  // Boot
  // ------------------------------------------------------------------- //

  refreshDevices().catch((err) => {
    console.error("failed to load devices", err);
  });
  // Refresh device list every 5s so control_state stays accurate.
  setInterval(() => { refreshDevices().catch(() => {}); }, 5000);
})();

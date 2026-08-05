package com.hearth.companion.features.onboarding

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.hearth.companion.HearthApp
import com.hearth.companion.core.LoginRequest
import com.hearth.companion.uistyle.HearthColors
import kotlinx.coroutines.launch

@Composable
fun LoginScreen(app: HearthApp, onDone: () -> Unit) {
    var password by remember { mutableStateOf("") }
    var errMsg by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()

    Column(
        Modifier.fillMaxSize().background(HearthColors.Void).padding(24.dp),
    ) {
        Text("Hearth password", color = HearthColors.Bone, style = MaterialTheme.typography.displayMedium)
        Text(
            "The password you set at first-boot on the Hearth itself. Never leaves the house.",
            color = HearthColors.BoneDim,
            modifier = Modifier.padding(vertical = 12.dp),
        )
        OutlinedTextField(
            value = password,
            onValueChange = { password = it; errMsg = null },
            placeholder = { Text("Hearth password", color = HearthColors.BoneDim) },
            singleLine = true,
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            colors = OutlinedTextFieldDefaults.colors(
                focusedTextColor = HearthColors.Bone,
                unfocusedTextColor = HearthColors.Bone,
                focusedBorderColor = HearthColors.Pal,
                unfocusedBorderColor = HearthColors.Line,
                cursorColor = HearthColors.Pal,
                focusedContainerColor = HearthColors.Ink,
                unfocusedContainerColor = HearthColors.Ink,
            ),
            modifier = Modifier.fillMaxWidth(),
        )
        errMsg?.let {
            Text(
                it,
                color = HearthColors.Ember,
                modifier = Modifier.padding(top = 8.dp),
                style = MaterialTheme.typography.labelLarge,
            )
        }
        Button(
            onClick = {
                scope.launch {
                    runCatching {
                        val client = app.buildClient() ?: error("Not paired")
                        val resp = client.api.login(LoginRequest(password))
                        app.store.saveCsrf(resp.csrf)
                        onDone()
                    }.onFailure { errMsg = it.message ?: "Login failed" }
                }
            },
            colors = ButtonDefaults.buttonColors(containerColor = HearthColors.Pal, contentColor = HearthColors.Void),
            enabled = password.length >= 6,
            modifier = Modifier.padding(top = 16.dp).fillMaxWidth(),
        ) { Text("Sign in to Hearth") }
    }
}

package com.hearth.companion

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Devices
import androidx.compose.material.icons.outlined.LibraryMusic
import androidx.compose.material.icons.outlined.People
import androidx.compose.material.icons.outlined.SettingsRemote
import androidx.compose.material.icons.outlined.Tune
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.hearth.companion.features.devices.DevicesListScreen
import com.hearth.companion.features.extenders.ExtendersListScreen
import com.hearth.companion.features.household.UsersScreen
import com.hearth.companion.features.library.LibraryScreen
import com.hearth.companion.features.onboarding.DiscoveryScreen
import com.hearth.companion.features.onboarding.LoginScreen
import com.hearth.companion.features.onboarding.QRPairScreen
import com.hearth.companion.features.settings.SettingsScreen
import com.hearth.companion.uistyle.HearthColors
import com.hearth.companion.uistyle.HearthTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val app = application as HearthApp
        setContent {
            HearthTheme {
                if (app.store.isPaired()) MainShell(app) else OnboardingShell(app)
            }
        }
    }
}

private enum class Tab(val route: String, val title: String, val icon: ImageVector) {
    Devices("devices", "Devices", Icons.Outlined.SettingsRemote),
    Household("household", "Household", Icons.Outlined.People),
    Library("library", "Library", Icons.Outlined.LibraryMusic),
    Extenders("extenders", "Embers", Icons.Outlined.Devices),
    Settings("settings", "Settings", Icons.Outlined.Tune),
}

@Composable
private fun MainShell(app: HearthApp) {
    val nav = rememberNavController()
    var current by remember { mutableStateOf(Tab.Devices) }

    Scaffold(
        modifier = Modifier.fillMaxSize().background(HearthColors.Void),
        containerColor = HearthColors.Void,
        bottomBar = {
            NavigationBar(containerColor = HearthColors.VoidLift, tonalElevation = 0.dp) {
                Tab.values().forEach { tab ->
                    NavigationBarItem(
                        selected = tab == current,
                        onClick = {
                            current = tab
                            nav.navigate(tab.route) {
                                launchSingleTop = true
                                popUpTo(Tab.Devices.route) { inclusive = false }
                            }
                        },
                        icon = { Icon(tab.icon, contentDescription = tab.title) },
                        label = { Text(tab.title) },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = HearthColors.Pal,
                            selectedTextColor = HearthColors.Pal,
                            indicatorColor = HearthColors.Ink,
                            unselectedIconColor = HearthColors.BoneDim,
                            unselectedTextColor = HearthColors.BoneDim,
                        )
                    )
                }
            }
        }
    ) { padding ->
        Box(Modifier.padding(padding).fillMaxSize()) {
            NavHost(navController = nav, startDestination = Tab.Devices.route) {
                composable(Tab.Devices.route) { DevicesListScreen(app) }
                composable(Tab.Household.route) { UsersScreen(app) }
                composable(Tab.Library.route) { LibraryScreen(app) }
                composable(Tab.Extenders.route) { ExtendersListScreen(app) }
                composable(Tab.Settings.route) { SettingsScreen(app) }
            }
        }
    }
}

@Composable
private fun OnboardingShell(app: HearthApp) {
    val nav = rememberNavController()
    NavHost(navController = nav, startDestination = "discover") {
        composable("discover") {
            DiscoveryScreen(app) { host, port ->
                nav.navigate("pair/${host}/${port}")
            }
        }
        composable("pair/{host}/{port}") { entry ->
            val host = entry.arguments?.getString("host") ?: return@composable
            val port = entry.arguments?.getString("port")?.toIntOrNull() ?: return@composable
            QRPairScreen(app, host, port) { nav.navigate("login") }
        }
        composable("login") {
            LoginScreen(app) { nav.navigate("done") }
        }
        composable("done") {
            Column(
                Modifier.fillMaxSize().background(HearthColors.Void),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally,
            ) { Text("Restart to continue.", color = HearthColors.Bone) }
        }
    }
}

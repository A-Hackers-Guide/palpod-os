package com.hearth.companion

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.unit.dp
import com.hearth.companion.core.consentClickable
import com.hearth.companion.uistyle.HearthTheme
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test

/**
 * A minimal Compose UI test that shows the pattern for exercising the
 * consent surface end-to-end.
 */
class OnboardingFlowTest {

    @get:Rule val compose = createComposeRule()

    @Test fun themeRendersText() {
        compose.setContent { HearthTheme { Text("Hearth Companion") } }
        compose.onNodeWithText("Hearth Companion").assertIsDisplayed()
    }

    @Test fun consentButtonClickProducesGesture() {
        var minted = 0
        compose.setContent {
            HearthTheme {
                Box(
                    modifier = Modifier
                        .size(120.dp)
                        .consentClickable(surface = "grant-15m") { minted += 1 }
                ) { Text("15 min") }
            }
        }
        compose.onNodeWithText("15 min").performClick()
        assertEquals(1, minted)
    }
}

package dev.m34nx.tsb

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import rikka.shizuku.Shizuku

private const val SHIZUKU_PACKAGE = "moe.shizuku.privileged.api"
private const val TERMUX_PACKAGE = "com.termux"

class MainActivity : ComponentActivity() {
    private fun isInstalled(packageName: String): Boolean =
        try {
            packageManager.getPackageInfo(packageName, 0)
            true
        } catch (_: PackageManager.NameNotFoundException) {
            false
        }

    private fun refreshSnapshot() = Snapshot(
        termuxInstalled = isInstalled(TERMUX_PACKAGE),
        shizukuInstalled = isInstalled(SHIZUKU_PACKAGE),
        shizukuRunning = Shizuku.pingBinder()
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            var snapshot by remember { mutableStateOf(refreshSnapshot()) }
            TsbTheme {
                Dashboard(snapshot, { snapshot = refreshSnapshot() },
                    { openPackage(SHIZUKU_PACKAGE) }, { copyReport(snapshot) })
            }
        }
    }

    private fun openPackage(packageName: String) {
        packageManager.getLaunchIntentForPackage(packageName)?.let(::startActivity)
    }

    private fun copyReport(snapshot: Snapshot) {
        val report = """
            TSB Mobile 0.1.0
            Termux installed: ${snapshot.termuxInstalled}
            Shizuku installed: ${snapshot.shizukuInstalled}
            Shizuku binder reachable: ${snapshot.shizukuRunning}
            Note: Checks app presence and Shizuku binder reachability only.
        """.trimIndent()
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        clipboard.setPrimaryClip(ClipData.newPlainText("TSB diagnostic report", report))
    }
}

private data class Snapshot(val termuxInstalled: Boolean, val shizukuInstalled: Boolean, val shizukuRunning: Boolean)

@Composable
private fun TsbTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = Color(0xFF62E6C1), secondary = Color(0xFF8CB8FF),
            background = Color(0xFF0A1015), surface = Color(0xFF121C24)
        ), content = content
    )
}

@Composable
private fun Dashboard(
    snapshot: Snapshot, onRefresh: () -> Unit,
    onOpenShizuku: () -> Unit, onCopyReport: () -> Unit
) {
    Surface(Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
        Column(
            Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text("TSB / MOBILE", color = MaterialTheme.colorScheme.primary, fontSize = 13.sp, fontWeight = FontWeight.Bold)
            Text("Connection\nobservatory", fontSize = 32.sp, lineHeight = 36.sp, fontWeight = FontWeight.Bold)
            Text("A local, privacy-first overview of your Termux and Shizuku setup.", color = Color(0xFFB2C0CA))
            Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface), shape = RoundedCornerShape(20.dp)) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("SYSTEM STATUS", fontWeight = FontWeight.Bold, color = Color(0xFF9EAFBC))
                        Spacer(Modifier.weight(1f))
                        Text(if (snapshot.shizukuRunning) "CONNECTED" else "CHECK NEEDED",
                            color = if (snapshot.shizukuRunning) MaterialTheme.colorScheme.primary else Color(0xFFFFC36B),
                            fontWeight = FontWeight.Bold, fontSize = 12.sp)
                    }
                    StatusRow("Termux app", snapshot.termuxInstalled, "App presence only")
                    StatusRow("Shizuku app", snapshot.shizukuInstalled, "App presence only")
                    StatusRow("Shizuku service", snapshot.shizukuRunning, "Binder reachability")
                    Text("This screen does not verify rish, its DEX companion, or remote command execution.",
                        color = Color(0xFF9EAFBC), fontSize = 12.sp)
                }
            }
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                Button(onClick = onRefresh, modifier = Modifier.weight(1f)) { Text("Refresh") }
                OutlinedButton(onClick = onOpenShizuku, modifier = Modifier.weight(1f)) { Text("Open Shizuku") }
            }
            Text("SETUP CHECKLIST", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            InfoCard("01  Install Termux", "Install Termux and its plugins from the same trusted distribution source.")
            InfoCard("02  Start Shizuku", "Use Shizuku's official setup flow. Wireless debugging setup is available on Android 11+.")
            InfoCard("03  Authorize Termux", "Grant Termux access from Shizuku's application authorization screen.")
            InfoCard("04  Export rish", "Use Shizuku's terminal-app integration to export rish and rish_shizuku.dex.")
            Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("LOCAL DIAGNOSTIC REPORT", fontWeight = FontWeight.Bold)
                    Text("Copies app-presence and binder-status checks only. No data is uploaded.", color = Color(0xFF9EAFBC), fontSize = 13.sp)
                    OutlinedButton(onClick = onCopyReport) { Text("Copy report") }
                }
            }
            Text("TSB Mobile 0.1.0 • No telemetry • Read-only", color = Color(0xFF728391), fontSize = 11.sp)
        }
    }
}

@Composable
private fun StatusRow(label: String, ok: Boolean, detail: String) {
    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.weight(1f)) {
            Text(label, fontWeight = FontWeight.SemiBold)
            Text(detail, color = Color(0xFF8FA0AD), fontSize = 12.sp)
        }
        Text(if (ok) "AVAILABLE" else "NOT FOUND",
            color = if (ok) Color(0xFF62E6C1) else Color(0xFFFFC36B),
            fontSize = 11.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
private fun InfoCard(title: String, body: String) {
    Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
        Column(Modifier.padding(16.dp)) {
            Text(title, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(5.dp))
            Text(body, color = Color(0xFF9EAFBC), fontSize = 13.sp)
        }
    }
}

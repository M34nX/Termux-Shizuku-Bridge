package dev.m34nx.tsb

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
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
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.runtime.CompositionLocalProvider
import rikka.shizuku.Shizuku

private const val SHIZUKU_PACKAGE = "moe.shizuku.privileged.api"
private const val TERMUX_PACKAGE = "com.termux"
private const val PREFS_NAME = "tsb_mobile_preferences"
private const val PREF_LANGUAGE = "persian"

private data class DeviceSnapshot(
    val termuxInstalled: Boolean,
    val shizukuInstalled: Boolean,
    val binderReachable: Boolean,
    val androidRelease: String,
    val sdk: Int,
    val manufacturer: String,
    val model: String
)

class MainActivity : ComponentActivity() {
    private val snapshotState = mutableStateOf(
        DeviceSnapshot(false, false, false, Build.VERSION.RELEASE ?: "unknown",
            Build.VERSION.SDK_INT, Build.MANUFACTURER ?: "unknown", Build.MODEL ?: "unknown")
    )

    private fun packageIsInstalled(packageName: String): Boolean = try {
        val info = if (Build.VERSION.SDK_INT >= 33) {
            packageManager.getPackageInfo(packageName, PackageManager.PackageInfoFlags.of(0))
        } else {
            @Suppress("DEPRECATION")
            packageManager.getPackageInfo(packageName, 0)
        }
        info.packageName.isNotBlank()
    } catch (_: PackageManager.NameNotFoundException) {
        false
    }

    private fun collectSnapshot(): DeviceSnapshot {
        val termux = packageIsInstalled(TERMUX_PACKAGE)
        val shizuku = packageIsInstalled(SHIZUKU_PACKAGE)
        val binder = if (shizuku) runCatching { Shizuku.pingBinder() }.getOrDefault(false) else false
        return DeviceSnapshot(
            termuxInstalled = termux,
            shizukuInstalled = shizuku,
            binderReachable = binder,
            androidRelease = Build.VERSION.RELEASE ?: "unknown",
            sdk = Build.VERSION.SDK_INT,
            manufacturer = Build.MANUFACTURER ?: "unknown",
            model = Build.MODEL ?: "unknown"
        )
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        snapshotState.value = collectSnapshot()
        setContent {
            var persian by remember {
                mutableStateOf(getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
                    .getBoolean(PREF_LANGUAGE, false))
            }
            TsbTheme {
                Dashboard(
                    snapshot = snapshotState.value,
                    persian = persian,
                    onRefresh = { snapshotState.value = collectSnapshot() },
                    onToggleLanguage = {
                        persian = !persian
                        getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
                            .edit().putBoolean(PREF_LANGUAGE, persian).apply()
                    },
                    onOpenShizuku = { openPackage(SHIZUKU_PACKAGE) },
                    onOpenTermux = { openPackage(TERMUX_PACKAGE) },
                    onCopyReport = { copyReport(snapshotState.value) }
                )
            }
        }
    }

    override fun onResume() {
        super.onResume()
        snapshotState.value = collectSnapshot()
    }

    private fun openPackage(packageName: String) {
        val launchIntent: Intent? = packageManager.getLaunchIntentForPackage(packageName)
        launchIntent?.let(::startActivity)
    }

    private fun copyReport(snapshot: DeviceSnapshot) {
        val report = """
            TSB Mobile 0.2.0
            Android: ${snapshot.androidRelease} (API ${snapshot.sdk})
            Device: ${snapshot.manufacturer} ${snapshot.model}
            Termux installed: ${snapshot.termuxInstalled}
            Shizuku installed: ${snapshot.shizukuInstalled}
            Shizuku binder reachable: ${snapshot.binderReachable}
            Scope: local package visibility and Shizuku binder reachability only.
            Not tested here: rish, companion DEX, remote UID, remote command execution.
        """.trimIndent()
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        clipboard.setPrimaryClip(ClipData.newPlainText("TSB diagnostic report", report))
    }
}

@Composable
private fun TsbTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = Color(0xFF65E7C5),
            secondary = Color(0xFF9BBEFF),
            background = Color(0xFF081117),
            surface = Color(0xFF14222B),
            surfaceVariant = Color(0xFF1B2D37)
        ),
        content = content
    )
}

private fun tr(persian: Boolean, english: String, farsi: String): String =
    if (persian) farsi else english

@Composable
private fun Dashboard(
    snapshot: DeviceSnapshot,
    persian: Boolean,
    onRefresh: () -> Unit,
    onToggleLanguage: () -> Unit,
    onOpenShizuku: () -> Unit,
    onOpenTermux: () -> Unit,
    onCopyReport: () -> Unit
) {
    CompositionLocalProvider(
        LocalLayoutDirection provides if (persian) LayoutDirection.Rtl else LayoutDirection.Ltr
    ) {
        Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
            Column(
                modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text("TSB  /  MOBILE", color = MaterialTheme.colorScheme.primary,
                            fontSize = 13.sp, fontWeight = FontWeight.Bold)
                        Text(tr(persian, "CONNECTION OBSERVATORY", "مرکز پایش اتصال"),
                            color = Color(0xFF91A7B4), fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                    }
                    OutlinedButton(onClick = onToggleLanguage) {
                        Text(if (persian) "English" else "فارسی")
                    }
                }

                Text(
                    tr(persian, "Your bridge.\nClearly understood.", "وضعیت اتصال\nبا جزئیات روشن"),
                    fontSize = 30.sp, lineHeight = 36.sp, fontWeight = FontWeight.Bold,
                    color = Color(0xFFF0F6F8)
                )
                Text(
                    tr(persian,
                        "A local overview of Termux, Shizuku and your Android environment.",
                        "نمایی محلی از وضعیت ترموکس، شیزوکو و محیط اندروید."),
                    color = Color(0xFFB2C2CB), fontSize = 14.sp
                )

                Card(
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                    shape = RoundedCornerShape(22.dp)
                ) {
                    Column(Modifier.fillMaxWidth().padding(18.dp),
                        verticalArrangement = Arrangement.spacedBy(15.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(tr(persian, "CONNECTION STATUS", "وضعیت اتصال"),
                                fontWeight = FontWeight.Bold, color = Color(0xFFA9BBC5))
                            Spacer(Modifier.weight(1f))
                            Text(
                                if (snapshot.binderReachable)
                                    tr(persian, "BINDER ONLINE", "بایندر فعال")
                                else tr(persian, "ACTION NEEDED", "نیازمند بررسی"),
                                color = if (snapshot.binderReachable) MaterialTheme.colorScheme.primary
                                    else Color(0xFFFFC56F),
                                fontWeight = FontWeight.Bold, fontSize = 11.sp
                            )
                        }
                        StatusRow(tr(persian, "Termux app", "برنامهٔ ترموکس"),
                            snapshot.termuxInstalled, persian)
                        StatusRow(tr(persian, "Shizuku app", "برنامهٔ شیزوکو"),
                            snapshot.shizukuInstalled, persian)
                        StatusRow(tr(persian, "Shizuku Binder", "بایندر شیزوکو"),
                            snapshot.binderReachable, persian)
                        Text(
                            tr(persian,
                                "Important: Binder reachability does not prove that rish or remote commands work.",
                                "توجه: دسترسی به بایندر به‌تنهایی کارکرد rish یا اجرای فرمان از راه دور را اثبات نمی‌کند."),
                            color = Color(0xFF9EAFBC), fontSize = 12.sp
                        )
                    }
                }

                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    Button(onClick = onRefresh, modifier = Modifier.weight(1f)) {
                        Text(tr(persian, "Refresh", "به‌روزرسانی"))
                    }
                    OutlinedButton(onClick = onOpenShizuku, modifier = Modifier.weight(1f)) {
                        Text(tr(persian, "Open Shizuku", "بازکردن شیزوکو"))
                    }
                }
                OutlinedButton(onClick = onOpenTermux, modifier = Modifier.fillMaxWidth()) {
                    Text(tr(persian, "Open Termux", "بازکردن ترموکس"))
                }

                SectionTitle(tr(persian, "DEVICE OVERVIEW", "اطلاعات دستگاه"))
                InfoCard(
                    tr(persian, "Android environment", "محیط اندروید"),
                    "${snapshot.manufacturer} ${snapshot.model}\n" +
                        "Android ${snapshot.androidRelease}  •  API ${snapshot.sdk}"
                )

                SectionTitle(tr(persian, "QUICK SETUP", "راهنمای راه‌اندازی"))
                InfoCard(tr(persian, "01  Install both apps", "۰۱  نصب هر دو برنامه"),
                    tr(persian, "Install Termux and Shizuku. Keep Termux and its plugins from the same distribution source.",
                        "ترموکس و شیزوکو را نصب کنید. ترموکس و افزونه‌های آن باید از یک منبع انتشار باشند."))
                InfoCard(tr(persian, "02  Start Shizuku", "۰۲  راه‌اندازی شیزوکو"),
                    tr(persian, "Follow Shizuku's official setup guide. Wireless debugging is supported on Android 11+.",
                        "از راهنمای رسمی شیزوکو پیروی کنید. راه‌اندازی با عیب‌یابی بی‌سیم در اندروید ۱۱ به بالا پشتیبانی می‌شود."))
                InfoCard(tr(persian, "03  Authorize Termux", "۰۳  مجازکردن ترموکس"),
                    tr(persian, "Authorize Termux in Shizuku's application list. TSB never grants this permission for you.",
                        "در فهرست برنامه‌های شیزوکو به ترموکس مجوز بدهید. TSB این مجوز را خودکار اعطا نمی‌کند."))
                InfoCard(tr(persian, "04  Export rish", "۰۴  خروجی‌گرفتن از rish"),
                    tr(persian, "Export the official rish helper and rish_shizuku.dex using Shizuku's terminal integration.",
                        "ابزار rish و فایل rish_shizuku.dex را از طریق یکپارچه‌سازی ترمینال شیزوکو دریافت کنید."))

                Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                    shape = RoundedCornerShape(20.dp)) {
                    Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
                        Text(tr(persian, "PRIVATE DIAGNOSTIC REPORT", "گزارش تشخیصی خصوصی"),
                            fontWeight = FontWeight.Bold)
                        Text(tr(persian,
                            "Copies device and app-status data to your clipboard. Nothing is uploaded.",
                            "اطلاعات دستگاه و وضعیت برنامه‌ها را در حافظهٔ موقت کپی می‌کند؛ چیزی بارگذاری نمی‌شود."),
                            color = Color(0xFF9EAFBC), fontSize = 13.sp)
                        Button(onClick = onCopyReport) {
                            Text(tr(persian, "Copy report", "کپی گزارش"))
                        }
                    }
                }

                Text(
                    tr(persian,
                        "TSB Mobile 0.2.0 • Local-only • No telemetry",
                        "TSB Mobile 0.2.0 • فقط محلی • بدون تله‌متری"),
                    color = Color(0xFF718693), fontSize = 11.sp
                )
            }
        }
    }
}

@Composable
private fun SectionTitle(title: String) {
    Text(title, color = MaterialTheme.colorScheme.primary, fontSize = 12.sp,
        fontWeight = FontWeight.Bold)
}

@Composable
private fun StatusRow(label: String, available: Boolean, persian: Boolean) {
    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
        Text(label, modifier = Modifier.weight(1f), fontWeight = FontWeight.SemiBold)
        Text(
            if (available) tr(persian, "AVAILABLE", "در دسترس")
            else tr(persian, "NOT DETECTED", "شناسایی نشد"),
            color = if (available) Color(0xFF65E7C5) else Color(0xFFFFC56F),
            fontSize = 10.sp, fontWeight = FontWeight.Bold
        )
    }
}

@Composable
private fun InfoCard(title: String, body: String) {
    Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        shape = RoundedCornerShape(16.dp)) {
        Column(Modifier.fillMaxWidth().padding(16.dp)) {
            Text(title, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(6.dp))
            Text(body, color = Color(0xFFA9BBC5), fontSize = 13.sp, lineHeight = 19.sp)
        }
    }
}

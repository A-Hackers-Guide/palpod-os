# Keep kotlinx-serialization descriptors
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.AnnotationsKt

-keep,includedescriptorclasses class com.hearth.companion.**$$serializer { *; }
-keepclassmembers class com.hearth.companion.** {
    *** Companion;
}
-keepclasseswithmembers class com.hearth.companion.** {
    kotlinx.serialization.KSerializer serializer(...);
}

# OkHttp / Retrofit safe defaults
-dontwarn okhttp3.internal.platform.**
-dontwarn org.conscrypt.**
-dontwarn org.bouncycastle.**
-dontwarn org.openjsse.**

# Preserve consent primitives — obfuscation is fine but we keep members
# referenced reflectively by tests.
-keep class com.hearth.companion.core.ConsentGesture { *; }
-keep class com.hearth.companion.core.ConsentTokenSource { *; }

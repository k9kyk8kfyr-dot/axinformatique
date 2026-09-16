AXinfo Ultimate v17 — iPhone FIXED

تم إصلاح مشكلة فتح المشروع على iPhone:
- sw.js القديم كان يطلب icon.svg و images.jpg، وهما غير موجودين ضمن الملفات المرسلة.
- أضفنا icon.svg.
- أزلنا اعتماد الخلفية على images.jpg.
- جعلنا Service Worker لا يفشل بالكامل إذا تعذر تحميل ملف واحد.
- تم الحفاظ على manifest وواجهة iPhone وبيانات localStorage.

مهم جداً:
لا يمكن تشغيل Service Worker/PWA بشكل كامل عند فتح HTML مباشرة من Files عبر file://.
يجب تشغيله من HTTPS أو localhost.

بعد رفع الملفات إلى نفس المجلد على استضافة HTTPS:
1. افتح AXinfo_Ultimate_v17_iPhone.html في Safari.
2. Share / مشاركة.
3. Add to Home Screen / إضافة إلى الشاشة الرئيسية.
4. افتح AXinfo من الشاشة الرئيسية.

/* ==========================================================================
   APARTMAN ASSISTANT — LANDING PAGE SCRIPT
   ==========================================================================
   Tartalom:
   1. Analytics / marketing azonosítók (TODO — ide kerülnek majd)
   2. Cookie hozzájárulás kezelése (Consent Mode v2)
   3. Scroll-reveal animáció (data-reveal elemekhez)
   4. CTA kattintás-követés (dataLayer esemény, ha van hozzájárulás)
   ========================================================================== */

(function () {
  "use strict";

  /* ------------------------------------------------------------------------
     1. TODO — ANALYTICS AZONOSÍTÓK
     Amint megvannak a tényleges azonosítók, illeszd be őket ide, majd told
     be a loadAnalytics() függvénybe a betöltő scripteket (lásd lentebb
     kommentezve egy GA4 példa).
     ------------------------------------------------------------------------ */
  var GA4_MEASUREMENT_ID = ""; // pl. "G-XXXXXXXXXX"
  var META_PIXEL_ID = "982039981469218";

  function loadAnalytics() {
    // --- Google Analytics 4 betöltése (csak elfogadás után) ---
    // if (GA4_MEASUREMENT_ID) {
    //   var s = document.createElement("script");
    //   s.async = true;
    //   s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA4_MEASUREMENT_ID;
    //   document.head.appendChild(s);
    //   gtag('js', new Date());
    //   gtag('config', GA4_MEASUREMENT_ID);
    // }

    // --- Meta Pixel betöltése (csak elfogadás után) ---
    if (META_PIXEL_ID) {
      !function(f,b,e,v,n,t,s){
        if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)
      }(window, document,'script','https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', META_PIXEL_ID);
      fbq('track', 'PageView');
    }
  }

  /* ------------------------------------------------------------------------
     2. COOKIE HOZZÁJÁRULÁS
     ------------------------------------------------------------------------ */
  var CONSENT_KEY = "aa_cookie_consent"; // "granted" | "denied"
  var banner = document.getElementById("cookie-banner");
  var acceptBtn = document.getElementById("cookie-accept");
  var rejectBtn = document.getElementById("cookie-reject");

  function updateConsent(granted) {
    if (typeof gtag === "function") {
      gtag("consent", "update", {
        analytics_storage: granted ? "granted" : "denied",
        ad_storage: granted ? "granted" : "denied",
        ad_user_data: granted ? "granted" : "denied",
        ad_personalization: granted ? "granted" : "denied",
      });
    }
    if (granted) {
      loadAnalytics();
    }
  }

  function getStoredConsent() {
    try {
      return localStorage.getItem(CONSENT_KEY);
    } catch (e) {
      return null;
    }
  }

  function storeConsent(value) {
    try {
      localStorage.setItem(CONSENT_KEY, value);
    } catch (e) {
      /* localStorage nem elérhető — a banner minden látogatáskor megjelenik */
    }
  }

  function initCookieBanner() {
    if (!banner) return;
    var stored = getStoredConsent();

    if (stored === "granted") {
      updateConsent(true);
      return;
    }
    if (stored === "denied") {
      updateConsent(false);
      return;
    }

    // Nincs korábbi döntés — megjelenítjük a bannert
    banner.classList.add("is-visible");

    if (acceptBtn) {
      acceptBtn.addEventListener("click", function () {
        storeConsent("granted");
        updateConsent(true);
        banner.classList.remove("is-visible");
      });
    }

    if (rejectBtn) {
      rejectBtn.addEventListener("click", function () {
        storeConsent("denied");
        updateConsent(false);
        banner.classList.remove("is-visible");
      });
    }
  }

  /* ------------------------------------------------------------------------
     3. SCROLL-REVEAL ANIMÁCIÓ
     Csak akkor fut, ha a böngésző támogatja az IntersectionObservert és a
     látogató nem kért csökkentett mozgást — enélkül minden elem simán,
     alapból látható marad (nincs layout-törés, ha a JS nem töltődik be).
     ------------------------------------------------------------------------ */
  function initScrollReveal() {
    var prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    var elements = document.querySelectorAll("[data-reveal]");

    if (
      prefersReducedMotion ||
      !("IntersectionObserver" in window) ||
      elements.length === 0
    ) {
      elements.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );

    elements.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ------------------------------------------------------------------------
     4. CTA KATTINTÁS-KÖVETÉS
     ------------------------------------------------------------------------ */
  function initCtaTracking() {
    var ctaButtons = document.querySelectorAll("[data-cta]");
    ctaButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (typeof window.dataLayer !== "undefined") {
          window.dataLayer.push({
            event: "cta_click",
            cta_location: btn.getAttribute("data-cta"),
          });
        }
      });
    });
  }

  /* ------------------------------------------------------------------------
     INDÍTÁS
     ------------------------------------------------------------------------ */
  document.addEventListener("DOMContentLoaded", function () {
    initCookieBanner();
    initScrollReveal();
    initCtaTracking();
  });
})();

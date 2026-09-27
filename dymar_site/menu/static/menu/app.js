document.addEventListener("DOMContentLoaded", function () {
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Sticky header shadow on scroll
  var header = document.querySelector("header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("scrolled", window.scrollY > 8);
    };
    document.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Scroll-reveal for sections/cards
  var revealEls = document.querySelectorAll(".reveal");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in-view"); });
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el) { observer.observe(el); });
  }

  // Toast helper
  var toast = document.getElementById("toast");
  var toastTimer;
  function showToast(text) {
    if (!toast) return;
    toast.textContent = text;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove("show"); }, 1800);
  }

  // AJAX "add to cart": intercept product-card forms, fall back to normal submit if fetch fails
  var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
  document.addEventListener("submit", function (e) {
    var form = e.target.closest(".pcard-form");
    if (!form) return;
    e.preventDefault();

    var btn = form.querySelector(".pcard-add");
    btn.classList.remove("bump");
    void btn.offsetWidth;
    btn.classList.add("bump");

    fetch(form.action, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrfToken,
      },
      body: new FormData(form),
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (data.ok) {
          showToast(data.item_name + " — додано в кошик");
          var countEl = document.getElementById("cart-count");
          if (countEl) {
            countEl.textContent = data.cart_count;
            countEl.classList.remove("bump");
            void countEl.offsetWidth;
            countEl.classList.add("bump");
          }
        }
      })
      .catch(function () {
        form.submit();
      });
  });
});

(function () {
    'use strict';

    // ---- Mobile menu + sticky nav state ----
    var nav = document.querySelector('.navbar');
    var burger = document.querySelector('.hamburger');
    var links = document.querySelector('.nav-links');

    if (burger && links) {
        burger.addEventListener('click', function () {
            var open = links.classList.toggle('open');
            burger.classList.toggle('open', open);
            burger.setAttribute('aria-expanded', open);
        });
        links.addEventListener('click', function (e) {
            if (e.target.tagName === 'A') {
                links.classList.remove('open');
                burger.classList.remove('open');
                burger.setAttribute('aria-expanded', 'false');
            }
        });
    }
    function onScroll() { if (nav) nav.classList.toggle('scrolled', window.scrollY > 24); }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // ---- Scroll reveal ----
    var items = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (en) {
                if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
            });
        }, { threshold: 0.12 });
        items.forEach(function (el) { io.observe(el); });
    } else {
        items.forEach(function (el) { el.classList.add('in'); });
    }

    // ---- Lightbox (mouse + keyboard) ----
    var box = document.getElementById('lightbox');
    if (box) {
        var big = document.getElementById('lightbox-img');
        var closeBtn = box.querySelector('.lightbox-close');
        var opener = null;
        var close = function () {
            box.classList.remove('open');
            if (opener) opener.focus();
        };
        var open = function (fig) {
            var img = fig.querySelector('img');
            opener = fig;
            big.src = img.currentSrc || img.src;
            big.alt = img.alt;
            box.classList.add('open');
            closeBtn.focus();
        };
        document.querySelectorAll('.lightbox-trigger').forEach(function (fig) {
            fig.addEventListener('click', function () { open(fig); });
            fig.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(fig); }
            });
        });
        closeBtn.addEventListener('click', close);
        box.addEventListener('click', function (e) { if (e.target !== big) close(); });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && box.classList.contains('open')) close();
        });
    }

    // ---- Quote form: sends to Travis by email (FormSubmit); falls back to the visitor's email app ----
    var EMAIL = 'travfraz@hotmail.com';
    document.querySelectorAll('.quote-form').forEach(function (form) {
        var ok = form.querySelector('.form-success');
        var err = form.querySelector('.form-error');
        var btn = form.querySelector('button[type="submit"]');
        var label = btn.textContent;

        function fallback(d) {
            var body = [
                'Name: ' + d.get('name'),
                'Phone: ' + d.get('phone'),
                'Email: ' + (d.get('email') || 'n/a'),
                'Service: ' + d.get('service'),
                '',
                'Project details:',
                d.get('details') || 'n/a'
            ].join('\n');
            window.location.href = 'mailto:' + EMAIL + '?subject=' +
                encodeURIComponent('Quote request: ' + d.get('service')) + '&body=' + encodeURIComponent(body);
        }

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var d = new FormData(form);
            if (d.get('_honey')) return;               // bot trap
            ok.style.display = 'none';
            err.style.display = 'none';
            btn.disabled = true;
            btn.textContent = 'Sending…';

            var payload = {};
            d.forEach(function (v, k) { if (k !== '_next') payload[k] = v; });

            fetch(form.dataset.endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify(payload)
            })
                .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
                .then(function (res) {
                    var good = res.ok && (res.j.success === true || res.j.success === 'true');
                    if (!good) throw new Error('not delivered');
                    form.reset();
                    ok.style.display = 'block';
                })
                .catch(function () {
                    err.style.display = 'block';
                    fallback(d);
                })
                .then(function () {
                    btn.disabled = false;
                    btn.textContent = label;
                });
        });
    });
})();

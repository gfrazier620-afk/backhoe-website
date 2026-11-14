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

    // ---- Lightbox ----
    var box = document.getElementById('lightbox');
    if (box) {
        var big = document.getElementById('lightbox-img');
        var close = function () { box.classList.remove('open'); };
        document.querySelectorAll('.lightbox-trigger').forEach(function (fig) {
            fig.addEventListener('click', function () {
                var img = fig.querySelector('img');
                big.src = img.currentSrc || img.src;
                big.alt = img.alt;
                box.classList.add('open');
            });
        });
        box.addEventListener('click', function (e) { if (e.target !== big) close(); });
        document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    }

    // ---- Quote form: opens an email to the company with the details filled in ----
    var EMAIL = 'travfraz@hotmail.com';
    document.querySelectorAll('.quote-form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var d = new FormData(form);
            var body = [
                'Name: ' + d.get('name'),
                'Phone: ' + d.get('phone'),
                'Email: ' + (d.get('email') || 'n/a'),
                'Service: ' + d.get('service'),
                '',
                'Project details:',
                d.get('details') || 'n/a'
            ].join('\n');
            var subject = 'Quote request: ' + d.get('service');
            window.location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
            var ok = form.querySelector('.form-success');
            if (ok) ok.style.display = 'block';
        });
    });
})();

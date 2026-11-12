const siteConfig = {
  // Replace these values with the approved Nuvex contact and profile URLs.
  contactEmail: "",
  social: {
    instagram: "",
    linkedin: "",
  },
  discord: "",
};

const menuButton = document.querySelector(".menu-toggle");
const primaryNav = document.querySelector("#primary-nav");

if (menuButton && primaryNav) {
  menuButton.addEventListener("click", () => {
    const isOpen = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!isOpen));
    primaryNav.classList.toggle("is-open", !isOpen);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
      menuButton.setAttribute("aria-expanded", "false");
      primaryNav.classList.remove("is-open");
      menuButton.focus();
    }
  });

  primaryNav.addEventListener("click", (event) => {
    if (event.target instanceof Element && event.target.closest("a")) {
      menuButton.setAttribute("aria-expanded", "false");
      primaryNav.classList.remove("is-open");
    }
  });
}

const socialLabels = {
  instagram: "Instagram",
  linkedin: "LinkedIn",
};

const contactEmailIsValid =
  /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(siteConfig.contactEmail);

if (siteConfig.contactEmail && !contactEmailIsValid) {
  console.error("Ungültige Kontakt-E-Mail-Adresse.");
  document.querySelectorAll("[data-contact-missing]").forEach((message) => {
    message.textContent = "Die Kontaktadresse ist ungültig konfiguriert.";
  });
}

if (contactEmailIsValid) {
  document.querySelectorAll("[data-contact-email]").forEach((link) => {
    link.href = `mailto:${siteConfig.contactEmail}`;
    link.textContent = siteConfig.contactEmail;
    link.hidden = false;
    const missing = link.parentElement?.querySelector("[data-contact-missing]");
    if (missing) missing.hidden = true;
  });
}

document.querySelectorAll("[data-social-links]").forEach((list) => {
  let linkCount = 0;
  let invalidCount = 0;
  Object.entries(siteConfig.social).forEach(([name, url]) => {
    if (!url) return;
    try {
      const parsed = new URL(url);
      const allowedHosts = {
        instagram: new Set(["instagram.com", "www.instagram.com"]),
        linkedin: new Set(["linkedin.com", "www.linkedin.com"]),
      };
      if (
        parsed.protocol !== "https:" ||
        !allowedHosts[name]?.has(parsed.hostname) ||
        parsed.username ||
        parsed.password
      ) {
        console.error(`Ungültige Social-URL für ${name}.`);
        invalidCount += 1;
        return;
      }

      const link = document.createElement("a");
      link.href = parsed.href;
      link.textContent = socialLabels[name] ?? name;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      list.append(link);
      linkCount += 1;
    } catch {
      console.error(`Ungültige Social-URL für ${name}.`);
      invalidCount += 1;
    }
  });

  const missing =
    list.parentElement?.querySelector("[data-social-missing]") ??
    list.parentElement?.querySelector(".footer-note");
  if (missing && invalidCount > 0) {
    missing.textContent = "Social-Link ungültig konfiguriert; bitte URL prüfen.";
    missing.hidden = false;
  } else if (missing && linkCount > 0) {
    missing.hidden = true;
  }
});

document.querySelectorAll("[data-discord]").forEach((link) => {
  if (!siteConfig.discord) return;
  try {
    const parsed = new URL(siteConfig.discord);
    if (
      parsed.protocol !== "https:" ||
      parsed.hostname !== "discord.gg" ||
      parsed.username ||
      parsed.password
    ) {
      console.error("Ungültige Discord-Einladungs-URL.");
      const missing = link.parentElement?.querySelector("[data-discord-missing]");
      if (missing) missing.textContent = "Discord-Link ungültig konfiguriert; bitte URL prüfen.";
      return;
    }
    link.href = parsed.href;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.hidden = false;
    const missing = link.parentElement?.querySelector("[data-discord-missing]");
    if (missing) missing.hidden = true;
  } catch {
    console.error("Ungültige Discord-Einladungs-URL.");
    const missing = link.parentElement?.querySelector("[data-discord-missing]");
    if (missing) missing.textContent = "Discord-Link ungültig konfiguriert; bitte URL prüfen.";
  }
});

document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = String(new Date().getFullYear());
});

const contactForm = document.querySelector("[data-contact-form]");
if (contactForm instanceof HTMLFormElement) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const status = contactForm.querySelector(".form-status");
    if (!contactEmailIsValid) {
      if (status) status.textContent = siteConfig.contactEmail
        ? "Die Kontaktadresse ist ungültig konfiguriert. Bitte verwende vorerst einen anderen Kontaktweg."
        : "Die Kontaktadresse ist noch nicht konfiguriert. Bitte verwende vorerst einen anderen Kontaktweg.";
      return;
    }

    const formData = new FormData(contactForm);
    const subject = `Kontaktanfrage von ${String(formData.get("name") ?? "").trim()}`;
    const body = [
      `Name: ${String(formData.get("name") ?? "").trim()}`,
      `E-Mail: ${String(formData.get("email") ?? "").trim()}`,
      `Unternehmen: ${String(formData.get("company") ?? "").trim() || "Nicht angegeben"}`,
      "",
      String(formData.get("message") ?? "").trim(),
    ].join("\n");
    window.location.href = `mailto:${siteConfig.contactEmail}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    if (status) status.textContent = "Dein E-Mail-Programm sollte sich jetzt öffnen. Die Nachricht wird erst dort nach dem Klick auf „Senden“ übermittelt.";
  });
}

import { placeMarker, reverseGeocode } from "./geocode.js";
import { getCookie } from "./csrf.js";

document.addEventListener("DOMContentLoaded", () => {
  const addressField = document.getElementById("addressField");
  const latField = document.getElementById("latField");
  const lngField = document.getElementById("lngField");
  const labelField = document.getElementById("labelField");
  const saveBtn = document.getElementById("saveBtn");
  const useMyLocationBtn = document.getElementById("useMyLocationBtn");

  const fallbackSpain = { lat: 40.4168, lng: -3.7038 };
  let map, marker, geocoder;

  function initMap(center) {
    const mapEl = document.getElementById("map");
    if (!mapEl) return; // ✅ evita error si no existe el div

    map = new google.maps.Map(mapEl, {
      center: center || fallbackSpain,
      zoom: center ? 14 : 6,
      mapTypeControl: false,
      streetViewControl: false,
    });
    geocoder = new google.maps.Geocoder();

    map.addListener("click", (e) => {
      marker = placeMarker(e.latLng, map, marker, latField, lngField, saveBtn, addressField);
      reverseGeocode(e.latLng, geocoder, addressField, latField, lngField, saveBtn);
    });
  }

  // Geolocalización inicial
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => initMap({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      () => initMap(fallbackSpain),
      { enableHighAccuracy: true, timeout: 8000 }
    );
  } else {
    initMap(fallbackSpain);
  }

  // Botón "Usar mi ubicación"
  if (useMyLocationBtn) {
    useMyLocationBtn.addEventListener("click", () => {
      if (!navigator.geolocation) return;
      navigator.geolocation.getCurrentPosition((pos) => {
        const latLng = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
        if (map) {
          map.setCenter(latLng);
          map.setZoom(15);
          marker = placeMarker(latLng, map, marker, latField, lngField, saveBtn, addressField);
          reverseGeocode(latLng, geocoder, addressField, latField, lngField, saveBtn);
        }
      });
    });
  }

  // Guardar dirección
  if (saveBtn) {
    saveBtn.addEventListener("click", async () => {
      const payload = {
        address: addressField?.value || "",
        latitude: parseFloat(latField?.value) || null,
        longitude: parseFloat(lngField?.value) || null,
        label: labelField?.value.trim() || ""
      };

      try {
        const res = await fetch("/locations/save/", { // ✅ ajusta a tu endpoint real
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
          },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
          alert("Dirección guardada");
          if (labelField) labelField.value = "";
        } else {
          alert(data.error || "Error al guardar la dirección");
        }
      } catch (err) {
        console.error(err);
        alert("Error de red al guardar");
      }
    });
  }
});

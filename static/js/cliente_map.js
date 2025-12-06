document.addEventListener("DOMContentLoaded", () => {
  const fallbackSpain = { lat: 40.4168, lng: -3.7038 };
  const addressField = document.getElementById("addressField");
  const latField = document.getElementById("latField");
  const lngField = document.getElementById("lngField");
  const labelField = document.getElementById("labelField");
  const saveBtn = document.getElementById("saveBtn");
  const useMyLocationBtn = document.getElementById("useMyLocationBtn");
  const nuevaDireccionBtn = document.getElementById("nuevaDireccionBtn");
  const direccionPrincipalSelect = document.getElementById("id_direccion_principal");
  const addrList = document.getElementById("addrList");

  // Variables dinámicas que vienen del template
  const clienteId = window.CLIENTE_ID;
  const direccionPrincipal = window.DIRECCION_PRINCIPAL;

  let map, marker, geocoder;

  function initMap(center) {
    map = new google.maps.Map(document.getElementById("map"), {
      center: center || fallbackSpain,
      zoom: center ? 14 : 6,
      mapTypeControl: false,
      streetViewControl: false,
    });
    geocoder = new google.maps.Geocoder();

    map.addListener("click", (e) => {
      placeMarker(e.latLng);
      reverseGeocode(e.latLng);
    });
  }

  function placeMarker(latLng) {
    if (!marker) {
      marker = new google.maps.Marker({
        position: latLng,
        map,
        draggable: true,
        animation: google.maps.Animation.DROP
      });
      marker.addListener("dragend", (e) => reverseGeocode(e.latLng));
    } else {
      marker.setPosition(latLng);
    }
    latField.value = latLng.lat().toFixed(6);
    lngField.value = latLng.lng().toFixed(6);
    saveBtn.disabled = !addressField.value;
  }

  function reverseGeocode(latLng) {
    geocoder.geocode({ location: latLng }, (results, status) => {
      if (status === "OK" && results && results.length) {
        addressField.value = results[0].formatted_address;
        latField.value = latLng.lat().toFixed(6);
        lngField.value = latLng.lng().toFixed(6);
        saveBtn.disabled = false;
      } else {
        addressField.value = "";
        saveBtn.disabled = true;
      }
    });
  }

  if (document.getElementById("collapseMap")) {
    document.getElementById("collapseMap").addEventListener("shown.bs.collapse", () => {
      if (!map) {
        const center = direccionPrincipal.lat ? { lat: direccionPrincipal.lat, lng: direccionPrincipal.lng } : fallbackSpain;
        initMap(center);
        if (direccionPrincipal.lat) {
          const latLng = new google.maps.LatLng(direccionPrincipal.lat, direccionPrincipal.lng);
          placeMarker(latLng);
          addressField.value = direccionPrincipal.address;
          latField.value = direccionPrincipal.lat;
          lngField.value = direccionPrincipal.lng;
          saveBtn.disabled = false;
        }
      }
    });
  }

  useMyLocationBtn?.addEventListener("click", () => {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition((pos) => {
      const latLng = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
      map.setCenter(latLng);
      map.setZoom(15);
      placeMarker(latLng);
      reverseGeocode(latLng);
    });
  });

  nuevaDireccionBtn?.addEventListener("click", () => {
    if (map) {
      map.setCenter(fallbackSpain);
      map.setZoom(6);
      if (marker) marker.setMap(null);
      marker = null;
    }
    addressField.value = "";
    latField.value = "";
    lngField.value = "";
    labelField.value = "";
    saveBtn.disabled = true;
  });

  saveBtn?.addEventListener("click", async () => {
    const payload = {
      address: addressField.value,
      latitude: parseFloat(latField.value),
      longitude: parseFloat(lngField.value),
      label: labelField.value.trim(),
      cliente_id: clienteId
    };

    try {
      const res = await fetch("/locations/api/direcciones/", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok) {
        const li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between align-items-center";
        li.innerHTML = `<span>${payload.label || "(sin etiqueta)"} — ${data.address}</span>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary set-principal" data-id="${data.id}">Hacer principal</button>
                        </div>`;
        addrList.prepend(li);

        if (direccionPrincipalSelect) {
          const opt = new Option(data.address, data.id, false, false);
          direccionPrincipalSelect.appendChild(opt);
          if (!direccionPrincipalSelect.value) {
            direccionPrincipalSelect.value = data.id;
          }
        }

        labelField.value = "";
        saveBtn.textContent = "Guardada";
        setTimeout(() => (saveBtn.textContent = "Guardar dirección"), 1200);
      } else {
        alert(data.error || "Error al guardar la dirección");
      }
    } catch (err) {
      console.error(err);
      alert("Error de red al guardar");
    }
  });

  document.addEventListener("click", async (e) => {
    if (!e.target.classList.contains("set-principal")) return;
    const id = e.target.dataset.id;
    if (direccionPrincipalSelect) {
      direccionPrincipalSelect.value = id;
    }
    if (clienteId) {
      try {
        const res = await fetch(`/clientes/${clienteId}/direccion-principal/`, {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
          body: JSON.stringify({ direccion_id: id })
        });
        const data = await res.json();
        if (!res.ok) {
          alert(data.error || "Error al marcar como principal");
        }
      } catch (err) {
        console.error(err);
        alert("Error de red al marcar principal");
      }
    }
  });

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  }
});

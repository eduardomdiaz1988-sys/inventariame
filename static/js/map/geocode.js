export function placeMarker(latLng, map, marker, latField, lngField, saveBtn, addressField) {
  if (!map) return marker;

  // Usa AdvancedMarkerElement si está disponible, si no, Marker clásico
  const MarkerClass = google.maps.marker?.AdvancedMarkerElement || google.maps.Marker;

  if (!marker) {
    marker = new MarkerClass({
      position: latLng,
      map,
      draggable: true,
    });

    marker.addListener("dragend", (e) => {
      reverseGeocode(e.latLng, new google.maps.Geocoder(), addressField, latField, lngField, saveBtn);
    });
  } else {
    marker.setPosition(latLng);
  }

  if (latField) latField.value = latLng.lat().toFixed(6);
  if (lngField) lngField.value = latLng.lng().toFixed(6);
  if (saveBtn) saveBtn.disabled = !addressField?.value;

  return marker;
}

export function reverseGeocode(latLng, geocoder, addressField, latField, lngField, saveBtn) {
  if (!geocoder) return;

  geocoder.geocode({ location: latLng }, (results, status) => {
    if (status === "OK" && results && results.length) {
      if (addressField) addressField.value = results[0].formatted_address;
      if (latField) latField.value = latLng.lat().toFixed(6);
      if (lngField) lngField.value = latLng.lng().toFixed(6);
      if (saveBtn) saveBtn.disabled = false;
    } else {
      if (addressField) addressField.value = "";
      if (saveBtn) saveBtn.disabled = true;
    }
  });
}

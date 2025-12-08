export function placeMarker(latLng, map, marker, latField, lngField, saveBtn, addressField) {
  if (!marker) {
    marker = new google.maps.Marker({
      position: latLng,
      map,
      draggable: true,
      animation: google.maps.Animation.DROP,
    });
    marker.addListener("dragend", (e) => {
      reverseGeocode(e.latLng, new google.maps.Geocoder(), addressField, latField, lngField, saveBtn);
    });
  } else {
    marker.setPosition(latLng);
  }

  latField.value = latLng.lat().toFixed(6);
  lngField.value = latLng.lng().toFixed(6);
  saveBtn.disabled = !addressField.value;
  return marker;
}

export function reverseGeocode(latLng, geocoder, addressField, latField, lngField, saveBtn) {
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

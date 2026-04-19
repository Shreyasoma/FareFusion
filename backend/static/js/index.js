const words = ['Compare.', 'Analyze.', 'Ride Smart.', 'Save More.'];

const typingElement = document.getElementById('typing-text');

let wordIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeEffect() {
  if (!typingElement) return;
  const currentWord = words[wordIndex];

  if (!isDeleting) {
    // Typing forward
    typingElement.textContent = currentWord.substring(0, charIndex + 1);
    charIndex++;

    if (charIndex === currentWord.length) {
      setTimeout(() => (isDeleting = true), 1000); // pause before deleting
    }
  } else {
    // Deleting
    typingElement.textContent = currentWord.substring(0, charIndex - 1);
    charIndex--;

    if (charIndex === 0) {
      isDeleting = false;
      wordIndex = (wordIndex + 1) % words.length;
    }
  }

  const speed = isDeleting ? 50 : 100;
  setTimeout(typeEffect, speed);
}

window.onload = typeEffect;

const toggleButton = document.getElementById('themeToggle');

if (toggleButton) {
  toggleButton.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');

    if (document.body.classList.contains('light-mode')) {
      toggleButton.textContent = '☀️';
    } else {
      toggleButton.textContent = '🌙';
    }
  });
}

const rideCards = document.querySelectorAll('.ride-card');
const rideInput = document.getElementById('rideType');

if (rideCards && rideInput) {
  rideCards.forEach((card) => {
    card.addEventListener('click', () => {
      // remove selected class from all cards
      rideCards.forEach((c) => c.classList.remove('selected'));

      // add selected class to clicked card
      card.classList.add('selected');

      // store selected ride type
      const rideType = card.dataset.ride;
      rideInput.value = rideType;
    });
  });
}

// Location Autocomplete Logic (Photon API)
function setupAutocomplete(inputId, listId) {
  const input = document.getElementById(inputId);
  const list = document.getElementById(listId);
  let timeoutId;

  if (!input || !list) return;

  // Close dropdown if clicked outside
  document.addEventListener('click', (e) => {
    if (e.target !== input && e.target !== list && !list.contains(e.target)) {
      list.style.display = 'none';
    }
  });

  input.addEventListener('input', () => {
    clearTimeout(timeoutId);
    const query = input.value.trim();

    if (query.length < 3) {
      list.style.display = 'none';
      list.innerHTML = '';
      return;
    }

    timeoutId = setTimeout(async () => {
      try {
        // Fetch matching locations from open-source Photon API
        const res = await fetch(`https://photon.komoot.io/api/?q=
          ${encodeURIComponent(query)}&limit=5`);
        const data = await res.json();

        list.innerHTML = '';
        if (data.features && data.features.length > 0) {
          data.features.forEach(feature => {
            const props = feature.properties;

            // Build clean address format
            const parts = [];
            if (props.name) parts.push(props.name);
            if (props.city && props.city !== props.name) parts.push(props.city);
            else if (props.town && props.town !== props.name) parts.push(props.town);
            if (props.state && props.state !== props.name) parts.push(props.state);
            if (props.country && parts.length < 3) parts.push(props.country);

            const displayName = parts.join(', ');

            const li = document.createElement('li');
            li.textContent = displayName;

            // When user clicks the suggestion
            li.addEventListener('click', () => {
              input.value = displayName;
              list.style.display = 'none';
            });

            list.appendChild(li);
          });
          list.style.display = 'block';
        } else {
          list.style.display = 'none';
        }
      } catch (err) {
        console.error('Autocomplete fetch error:', err);
      }
    }, 400); // 400ms debounce typing
  });
}

// Initialize autocomplete on our boxes
setupAutocomplete('source', 'source-list');
setupAutocomplete('destination', 'destination-list');

// Location Auto-Detect UI Logic
async function detectUserLocation() {
  const locationBadge = document.getElementById('current-location');
  if (!locationBadge) return; // Feature only intended on dashboard

  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(async (position) => {
      try {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        // Use free OpenStreetMap Nominatim API for reverse geocoding
        const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
        const data = await response.json();

        if (data && data.address) {
          // Extract the most relevant city/neighborhood
          const cityOrArea = data.address.city || data.address.town || data.address.state_district || data.address.state;

          if (cityOrArea) {
            locationBadge.style.display = 'flex';
            locationBadge.innerHTML = `📍 ${cityOrArea}`;
          }
        }
      } catch (error) {
        console.error("Error fetching location data: ", error);
      }
    }, (error) => {
      console.warn("User denied location access or error occurred", error);
    });
  }
}

// Fire location detection
detectUserLocation();

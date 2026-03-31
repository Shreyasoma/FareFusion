const words = ['Compare.', 'Analyze.', 'Ride Smart.', 'Save More.'];

const typingElement = document.getElementById('typing-text');

let wordIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeEffect() {
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

toggleButton.addEventListener('click', () => {
  document.body.classList.toggle('light-mode');

  if (document.body.classList.contains('light-mode')) {
    toggleButton.textContent = '☀️';
  } else {
    toggleButton.textContent = '🌙';
  }
});

const rideCards = document.querySelectorAll('.ride-card');
const rideInput = document.getElementById('rideType');

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

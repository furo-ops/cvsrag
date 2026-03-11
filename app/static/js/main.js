// Toggle expanded card section
function toggleExpand(profileId) {
  const el = document.getElementById(`expand-${profileId}`);
  const btn = el.previousElementSibling.querySelector('.btn-expand');
  if (el.style.display === 'none') {
    el.style.display = 'block';
    btn.textContent = 'Collapse';
  } else {
    el.style.display = 'none';
    btn.textContent = 'View profile';
  }
}

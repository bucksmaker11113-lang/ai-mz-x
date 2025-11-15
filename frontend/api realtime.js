// api/realtime.js
// MZ/X – Frontend API wrapper a backend /realtime végpontjához

export async function fetchRealtime() {
  try {
    const res = await fetch("/realtime");
    return await res.json();
  } catch (err) {
    console.error("Realtime API hiba:", err);
    return null;
  }
}

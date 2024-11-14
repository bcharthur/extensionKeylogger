document.getElementById("launchButton").addEventListener("click", async () => {
  try {
    const response = await fetch("http://localhost:5000/start_paint");
    if (response.ok) {
      alert("Paint a été lancé avec succès !");
    } else {
      alert("Erreur lors du lancement de Paint.");
    }
  } catch (error) {
    alert("Impossible de se connecter au serveur pour lancer Paint.");
    console.error("Erreur :", error);
  }
});

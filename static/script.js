// script.js

document.getElementById('promptForm').addEventListener('submit', async (e) => {
  e.preventDefault()

  const prompt = document.getElementById('prompt').value
  const model = document.getElementById('model').value
  const responseText = document.getElementById('responseText')
  const audioPlayer = document.getElementById('audioPlayer')
  const errorMessage = document.getElementById('errorMessage')

  responseText.textContent = ''
  errorMessage.textContent = ''
  audioPlayer.style.display = 'none'

  const formData = new FormData()
  formData.append('prompt', prompt)
  formData.append('model', model)

  try {
    const res = await fetch('/talk', {
      method: 'POST',
      body: formData
    })

    const data = await res.json()

    if (!res.ok) {
      errorMessage.textContent = data.error || 'Unknown error occurred.'
      return
    }

    responseText.textContent = data.text
    audioPlayer.src = data.audio_url
    audioPlayer.style.display = 'block'
    audioPlayer.play()
  } catch (err) {
    errorMessage.textContent = 'Server error: ' + err.message
  }
})

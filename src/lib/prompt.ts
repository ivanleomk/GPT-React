"use server"

export const SubmitPrompt = async (userPrompt: string) => {
    console.log(`Received User Prompt of ${userPrompt}`)
    const res = await fetch("http://127.0.0.1:8000/", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            prompt: userPrompt
        })
    })
    return res.json()
}

export const ClearComponent = async () => {
    console.log("----Triggered this")
    const res = await fetch("http://127.0.0.1:8000/clear")
    console.log(res.json())
}
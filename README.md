# Introduction

To run this, you'll need to run the backend and the frontend. I used bun but any node runtime should work fine too. You'll also need to create a .env file in the `backend` folder

```
OPENAI_KEY=#key goes here
```

1. First, install the packages

```
bun install
```

2. Next run the frontend server

```
bun run dev
```

3. Start up our backend code

```
cd backend
python3 -m venv .virtual
source .virtual/bin/activate
pip3 install -r requirements.txt
uvicorn main:app --reload
```

It should work nicely from there on.

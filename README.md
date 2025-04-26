![github-submission-banner](https://github.com/user-attachments/assets/a1493b84-e4e2-456e-a791-ce35ee2bcf2f)

# 🚀 EchoPersona

> The brain behind your AI-powered Multiverse Utility Agent - Groq-fueled, Monad-enhanced, and Base-integrated.

---

## 📌 Problem Statement

**Problem Statement 1 - Weave AI magic with Groq**<br/>
**Problem Statement 2 - Unleash blockchain gameplay with Monad**<br/>
**Problem Statement 4 - Craft the Future of Onchain Consumer Experience with Base**

---

## 🎯 Objective

EchoPersona solves the problem of missed or delayed communication in both personal and professional settings by acting as your intelligent "second body." It serves busy professionals, entrepreneurs, and creators who want to maintain a consistent digital presence—even when they’re offline or away.

The project addresses a real-world need for responsive and personalized communication by generating context-aware, persona-aligned replies in your unique tone and style. Whether it's handling emails, chat messages, or social interactions, EchoPersona ensures you're always present—even when you're not.

By mimicking your communication style using AI, it adds tremendous value in terms of time management, brand consistency, and digital engagement. It also integrates subscription-based access, making it scalable and flexible for users with varying needs.

👤 Example Scenario
Imagine you're a content creator attending a weekend retreat with limited internet access. During this time, a brand you're collaborating with reaches out to finalize a campaign detail. Instead of leaving them on read or replying in a rush, EchoPersona automatically generates a response that aligns with your usual tone—friendly, witty, and on-brand—assuring them you'll follow up on Monday with the final assets. The brand feels heard, your professionalism stays intact, and your mental space stays clear.

---

## 🧠 Team & Approach

### Team Name:

I am a solo participant.

### Team Members:

- Aditya SwayamSiddha
  - GitHub : https://github.com/TheCoderAdi/
  - LinkedIn : https://linkedin.com/in/aditya-swayamsiddha-576ab426a
  - Role : Full-Stack Developer, AI Engineer, and Creative Technologist
    (Sole builder, designer, and developer of EchoPersona)

### 🧭 Your Approach

#### 🔍 Why I Chose This Problem

I've always been fascinated by the idea of having a digital twin—something that could represent me authentically when I'm not available. In today's always-on world, being responsive and consistent is both expected and exhausting. I wanted to build an AI agent that could understand _how_ I communicate, not just _what_ I say, and use that to help me stay present even when I'm away. EchoPersona is a response to that vision: a second body that speaks in my voice, holds my intent, and supports my personal and professional communication.

#### ⚔️ Key Challenges I Addressed

- **Capturing personalized tone & style**: One of the toughest challenges was training the AI to reflect my unique communication style and context, rather than generic responses.
- **Handling away-mode interactions**: Building a system that can respond intelligently when I’m unavailable without sounding robotic.
- **Seamless integration**: Combining FastAPI, MongoDB, Pinecone, smart contracts on Base, and Coinbase Wallet integration into a cohesive experience—all while keeping it solo and manageable.
- **Multimodal features**: Adding support for content creation (story NFTs) and gamified interactions (PvP) without bloating the user experience.

#### 💡 Pivots, Brainstorms, and Breakthroughs

- Initially, I planned just a persona-based auto-responder. But after brainstorming use cases, I expanded it into a full communication assistant—capable of email drafting, shopping help, and even NFT story minting via **Monad**.
- A major breakthrough was integrating Pinecone for style-aware memory. This allowed the AI to recall and match communication patterns with high contextual accuracy.
- To increase interactivity, I built **EchoMaze**—a collaborative maze exploration game where users can join as Player A or B, navigate using up/down/left/right controls, and try to guess or discover the hidden path. It's a lightweight, real-time PvP experience that brings users together in a fun, strategic way.
- Implementing smart contract–based subscriptions using **Base + Coinbase Wallet** added a new layer of utility and real-world readiness.

---

## 🛠️ Tech Stack

### Core Technologies Used:

- Frontend: Next.js, Tailwind CSS, shadcn/ui, onchainkit
- Backend: FastAPI (Python), JWT Authentication, REST APIs
- Database: MongoDB, Pinecone
- APIs: Groq, Base, Monad, Multer, Serpai, HuggingFace
- Hosting: Vercel (Frontend), Render (Backend), MongoDB Atlas, Pinata (IPFS for NFTs)

### Sponsor Technologies Used (if any):

- [✅] **Groq:** _How you used Groq_

  - Leveraged for ultra-fast LLM inference to power the core AI agent in EchoPersona. Groq enables ultra-fast, real-time persona-based responses for away mode, creative storytelling, product search, and summarization—allowing the AI to act as an intelligent, expressive second self when you're unavailable.

- [✅] **Monad:** _Your blockchain implementation_

  - Story NFT Minting – The agent transforms creative outputs into mintable NFTs using Monad’s blockchain. Metadata is stored on IPFS and finalized on-chain.

  - EchoMaze PvP Game – A maze-based multiplayer game where users take turns guessing the path using directional controls. Game state logic and reward interactions are designed to integrate with Monad’s smart contract layer.

- [✅] **Base:** _AgentKit / OnchainKit / Smart Wallet usage_

  - Used for deploying smart contracts to manage subscription plans (Basic, Premium, Pro).

  - OnchainKit was used to handle wallet interactions, enabling users to connect their Coinbase Wallet, authenticate, and subscribe directly from the frontend.
  - This brings seamless Web3 login and payment functionality into EchoPersona’s user flow.

> Note: Did not use Fluvio, Stellar, or Screenpipe in this build.

---

## ✨ Key Features

Highlighting the most important features of **EchoPersona**, your intelligent second self:

- ✅ **Persona-Based Auto-Responder (Away Mode)**  
  Your AI twin replies to messages in your tone and style when you're unavailable—powered by Groq + Pinecone to maintain memory and personality consistency.

- ✅ **Creative Agent + Story NFT Minting**  
  Turn your ideas into short stories and mint them as NFTs on Monad. Metadata is stored on IPFS and published on-chain.

- ✅ **EchoMaze – PvP Maze Game**  
  A multiplayer maze-guessing game. Players use directional controls to navigate and uncover the path. Monad-backed logic ensures fairness and future reward tracking.

- ✅ **Web3 Login + Subscription System**  
  Users connect via **Coinbase Wallet** using **OnchainKit** and subscribe to Basic, Premium, or Pro plans using smart contracts on Base.

- ✅ **AI Draft Email & Summary Generator**  
  EchoPersona can auto-draft replies or entire emails and summarize the messages for you when you're away—ideal for catching up without overload.

- ✅ **AI Shopping Assistant**  
  EchoPersona suggests products based on your intent, mood.Comes with product suggestions powered by SerpAI.

---

**Add visuals:**

- Chat UI showing auto-replies

  - ![ezgif-256fb04375ec7a](https://github.com/user-attachments/assets/5cdd18e7-c30c-4211-866c-3f2742fc1c27)

- NFT mint success screen

  - ![ezgif-2d0a95931e73ac](https://github.com/user-attachments/assets/630fe7ee-90cc-4968-8ca6-afc0d6e5dceb)

- Maze game with up/down/left/right buttons

  - ![ezgif-2bdcd0ee2a10dc](https://github.com/user-attachments/assets/3b573401-a744-46ba-90e8-3215c1a2379f)

- Coinbase wallet connection
  - ![ezgif-232d16cfc9aa7e](https://github.com/user-attachments/assets/f1ee57d6-ebc8-4900-b527-43e2246be072)
- Draft email screen

  - ![ezgif-4e8e47c54a717b](https://github.com/user-attachments/assets/32c400ae-42ba-4f5f-9b21-8da483068699)

- Shopping suggestions
  - ![ezgif-5de4199b0c6a35](https://github.com/user-attachments/assets/cd35035f-396d-431c-b8a2-e5336f236434)

---

## 📽️ Demo & Deliverables

- **Demo Video Link:** https://youtu.be/ARLEcCTMl5E
- **Pitch Deck / PPT Link:** https://1drv.ms/p/c/b68c14dd441fad9d/ETrTgbVJujBLmxdvj8t9n20BhvpLFQMZ0xNxL2ht9yLVjg?e=x5Hmio&nav=eyJzSWQiOjI1N30

---

## ✅ Tasks & Bonus Checklist

- [✅] **All members of the team completed the mandatory task - Followed at least 2 of our social channels and filled the form** (Details in Participant Manual)
- [✅] **All members of the team completed Bonus Task 1 - Sharing of Badges and filled the form (2 points)** (Details in Participant Manual)
- [✅] **All members of the team completed Bonus Task 2 - Signing up for Sprint.dev and filled the form (3 points)** (Details in Participant Manual)

_(Mark with ✅ if completed)_

---

## 🧪 How to Run the Project

There are 2 Repos.This is the backend repo.

> Access the frontend repo https://github.com/TheCoderAdi/EchoPersona

### Requirements:

- Python (v3.8 or higher recommended)
- Git

- API Keys (if any)
  Absolutely! Here's the improved **Requirements** section with links for getting each API key or access token, where applicable:

---

### ✅ Requirements

- **Python** (v3.8 or higher recommended)  
  [Download Python](https://www.python.org/downloads/)

- **Git**  
  [Install Git](https://git-scm.com/downloads)

---

### 🔐 API Keys

| 🔑 Environment Variable | 📋 Description                               | 🌐 Where to Get It                                                     |
| ----------------------- | -------------------------------------------- | ---------------------------------------------------------------------- |
| `GROQ_API_KEY`          | API key for using Groq inference engine      | [Get Groq API Key](https://console.groq.com/)                          |
| `PINECONE_KEY`          | API key for vector DB (Pinecone)             | [Get Pinecone API Key](https://app.pinecone.io/)                       |
| `OWNER_PRIVATE_KEY`     | Your wallet’s private key                    | Export from your wallet (MetaMask / Coinbase Wallet), **keep secure**  |
| `PINATA_JWT`            | JWT token for interacting with Pinata (IPFS) | [Get Pinata JWT](https://app.pinata.cloud/developer-tools)             |
| `OWNER_ADDRESS`         | Your wallet public address                   | From MetaMask / Coinbase Wallet                                        |
| `SERPAPI_API_KEY`       | API key for search results using SerpAPI     | [Get SerpAPI Key](https://serpapi.com/dashboard)                       |
| `BASE_PLAN_ADDRESS`     | Smart contract address for base plan         | you can deploy the contract                                            |
| `MAZE_CONTRACT_ADDRESS` | Contract address for Maze                    | you can deploy the contract                                            |
| `STORY_NFT_ADDRESS`     | Contract address for Maze                    | you can deploy the contract                                            |
| `SECRET_KEY`            | Secret key for FastAPI sessions              | Can be generated or set manually                                       |
| `FASTAPI_ENDPOINT`      | Endpoint that receives messages              | Usually your deployed FastAPI URL + `/receive-message`                 |
| `MONGO_URI`             | Your MongoDB connection string               | [Create Cluster on MongoDB Atlas](https://www.mongodb.com/cloud/atlas) |
| `CORS_ORIGIN`           | Frontend domain for CORS setup               | Typically `http://localhost:3000` during development                   |

- .env file setup (if needed)

```bash
GROQ_API_KEY=your-groq-api-key
PINECONE_KEY=your-pinecone-key
OWNER_PRIVATE_KEY=your-wallet-private-key
PINATA_JWT=your-pinata-jwt
OWNER_ADDRESS=your-wallet-address
SERPAPI_API_KEY=your-serpapi-api-key
BASE_PLAN_ADDRESS=your-deployed-address
MAZE_CONTRACT_ADDRESS=your-deployed-address
STORY_NFT_ADDRESS=your-deployed-address
SECRET_KEY=your-secret-key
FASTAPI_ENDPOINT=your-backend-url/receive-message
MONGO_URI=your-mongodb-url
CORS_ORIGIN=your-frontend-url
```

### Local Setup:

```bash
# Clone the repo
git clone https://github.com/TheCoderAdi/EchoPersona-Backend

# Install dependencies
cd EchoPersona-Backend
python -m venv .venv

# Activate the virtual environment (Windows-specific path)
source .venv/Scripts/activate  # On Windows (Git Bash or WSL)
# OR if you're on Unix/macOS:
# source .venv/bin/activate

# Install dependencies (fixing the command)
pip install -r requirements.txt

# Create a .env file
paste the above keys in the .env file

# Start development server
uvicorn main:app --reload
```

### My Deployed Contracts:
- EchoPersonaPlan Contract (On Base) - https://base-sepolia.blockscout.com/address/0x44D3C2F96128d1be60431cA0a062218003ffd100
- MazeGame Contract (On Monad) - https://testnet.monadexplorer.com/address/0xd7D156c4c244a606757F2D13DA0cb997cFAf8c2A
- StoryNFT Contract (On Monad) - https://testnet.monadexplorer.com/token/0x117981C7fEAaEaA9a24261f57DC76D1aEa3C05A3?tab=Items

---

## 🧬 Future Scope

List improvements, extensions, or follow-up features:

- 📈 **More Integrations:** Expand to include calendar sync, Slack bots, and richer marketplace recommendations.
- 🛡️ **Security Enhancements:** Encrypt more layers of user data, improve persona-based auth, and add rate-limiting & abuse protection.
- 🌐 **Localization & Accessibility:** Multilingual support, screen-reader friendly UI, and inclusive design for broader reach.
- 🧠 **Agent Memory Training:** Let users correct or refine their AI twin’s responses to improve over time.
- 🎮 **EchoMaze Upgrade:** Add real token rewards, dynamic maze generation, and live chat within the game.

---

## 📎 Resources / Credits

- **APIs & Tools:**

  - Groq (LLM inference)
  - Pinecone (vector memory)
  - IPFS (metadata storage)
  - Coinbase Wallet SDK / OnchainKit
  - Monad & Base blockchains
  - Shadcn/UI, TailwindCSS, React, Next.js

- **Open Source Libraries:**

  - Axios, Mongoose
  - Radix Icons, react-hot-toast, nivo/pie, radix-ui, canvas-confetti, lucide-react, motion

- **Acknowledgements:**  
  Shoutout to Groq, Monad, and Base for incredible dev tools, and to the hackathon community for the energy and support!

---

## 🏁 Final Words

Building **EchoPersona** was both a solo sprint and a deeply personal experiment.  
From persona modeling and real-time AI responses to integrating NFT minting and wallet-based subscriptions—I wore many hats, hit walls, pivoted hard, and learned fast.

The most fun part? Watching my AI twin generate stories I’d never write myself.  
The toughest? Debugging wallet connection flows at 2AM.  
The best part? It works—and I’d do it again in a heartbeat 💙

Huge thanks to the organizers and sponsors—this project is just the beginning.

---

# CodeSurgeon Frontend

React + TypeScript frontend for CodeSurgeon AI Bug Repair Agent.

## Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Configure environment (edit .env with your backend URL)
```

### Development

```bash
# Start dev server (http://localhost:3000)
npm run dev
```

### Building

```bash
# Build for production
npm run build

# Preview build
npm run preview
```

## Project Structure

```
src/
├── components/       # React components
│   ├── Dashboard.tsx        # Main dashboard component
│   ├── AnalysisForm.tsx     # PR/code input form
│   ├── BugsList.tsx         # List of detected bugs
│   ├── BugDetail.tsx        # Bug details and fixes
│   ├── ResultsSummary.tsx   # Analysis summary
│   └── LoadingSpinner.tsx   # Loading UI
├── pages/            # Page components
├── services/         # API and utility services
│   └── api.ts       # Backend API client
├── store/            # State management (Zustand)
│   └── analysisStore.ts
├── types/            # TypeScript type definitions
├── App.tsx           # Main app component
├── main.tsx          # React entry point
└── index.css         # Global styles (Tailwind)
```

## Features

- **Code Analysis**: Submit GitHub PR URLs or code snippets
- **Bug Detection**: Automated bug detection using AI
- **Fix Suggestions**: Get AI-generated code fixes
- **Alternative Solutions**: View multiple fix approaches
- **Real-time UI**: Interactive dashboard with live results

## API Integration

Frontend communicates with backend API at configured base URL:
- Default: `http://localhost:8000`
- Configure via `.env` file with `VITE_API_URL`

## Technologies

- React 18
- TypeScript
- Tailwind CSS
- Zustand (State Management)
- Axios (HTTP Client)
- Vite (Build Tool)

## Troubleshooting

### CORS Errors
- Ensure backend is running and CORS is properly configured
- Check `VITE_API_URL` matches your backend URL

### Blank Page
- Check browser console for errors
- Verify API endpoint is correct
- Restart dev server: `npm run dev`

### Styling Issues
- Ensure Tailwind CSS is properly configured
- Check `tailwind.config.ts` includes correct content paths
- Clear cache: `npm run build && npm run preview`

## Environment Variables

```
VITE_API_URL=http://localhost:8000  # Backend API URL
VITE_ENV=development                 # Environment (development/production)
```

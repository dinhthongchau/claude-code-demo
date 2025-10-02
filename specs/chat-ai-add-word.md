# AI Chat Add Word Feature

## Functionality
- Chat with AI to learn and add vocabulary to folders
- AI explains words with definitions and examples
- Each AI response includes a folder button for easy word saving
- Users can select target folder and customize word details before adding

## Backend

### Requirements
- Create endpoint for AI chat conversation
- AI analyzes user messages and provides word explanations
- Generate word entries with definitions and examples
- Endpoint to add words to global words and add words to user's selected folders
- Return AI explanations with word metadata

## Mobile

### Requirements
- Add AI chat button floating  in main screen
- Create chat interface with message bubbles
- Display folder button next to AI word explanations
- Modal for folder selection and word customization
- Allow editing of word meanings and examples before saving

### User Flow
1. User taps AI bubble chat button on screen
2. User asks AI about a specific word (e.g., "Necessary")
3. AI responds with word explanations and examples
4. User taps folder button to open edit screen with word details
5. User can edit meaning, examples, choose images, and select target folder
6. After saving, word is added to the selected user folder


### Floating Button
- Position: Bottom right of ListFolderScreen
- Icon: AI/Chat icon
- Action: Open ChatModal

## Technical Notes
- Use  OpenAI key API
- Use pixabay key api
- Reuse add word to words
- Reuse add-word-to-list API
- Chat history no need to store
- /api/v1/users/{TEST_USER_ID}/folders/{TEST_FOLDER_ID}/wordlist

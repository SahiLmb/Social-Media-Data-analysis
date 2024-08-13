# WhatsApp Chat Analyzer

## Overview

The **WhatsApp Chat Analyzer** is a tool built with Streamlit to analyze WhatsApp chat data. The application allows users to upload a WhatsApp chat file and provides various insights, including message statistics, user activity, and sentiment analysis. It supports both English and Hinglish (a mix of Hindi and English) for sentiment analysis.

## Features

- **User Activity Analysis**: Identify the most active users in a chat group or analyze individual user activity.
- **Message Statistics**: Get counts of total messages, words, media, deleted messages, and shared links.
- **Sentiment Analysis**: Analyze the sentiment of chat messages, distinguishing between positive, negative, and neutral messages. Smiling and angry emojis are used to represent overall sentiment.
- **Word Cloud**: Generate a word cloud to visualize the most common words used in the chat.
- **Customizable Visuals**: Bar charts, pie charts, and word clouds with vibrant colors and detailed labels.

## Installation

### Prerequisites

- Python 3.7 or higher
- `pip` package manager

### Clone the Repository

```bash
git clone https://github.com/SahiLmb/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

## Usage

1. **Prepare Your WhatsApp Chat File**: Export your WhatsApp chat history as a `.txt` file.

2. **Run the Streamlit App**:

   ```bash
   streamlit run app.py
   ```

3. **Upload Your Chat File**: Use the sidebar in the Streamlit app to upload your WhatsApp chat file.

4. **Analyze the Chat**: Select the user or group for analysis and click the "Analyze the chat" button. The app will display various statistics and visualizations.

## Sentiment Analysis

- The app includes a custom sentiment analysis tool that can handle Hinglish (Hindi + English).
- Sentiments are classified as **positive**, **negative**, or **neutral**.
- A pie chart is used to visualize the distribution of sentiments, with a smiling emoji (😊) for positive sentiments and an angry emoji (😡) for negative sentiments.

## Customization

You can customize the following aspects of the project:
- **Hinglish to English Sentiment Mapping**: Modify the `hinglish_to_english` dictionary in `helper.py` to include more translations.
- **Stopwords and Exclusions**: Add or remove words that should be excluded from the word cloud and common words list.

## Future Enhancements

- **Multi-language Support**: Extend sentiment analysis to other languages.
- **Advanced Analytics**: Incorporate machine learning models for more sophisticated analysis.
- **Export Options**: Allow users to export the analyzed data and visualizations.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For any inquiries, please contact [work.bodke@gmail.com](mailto:your-email@example.com).

---

This README provides a comprehensive overview of the project, guiding users on how to install, use, and contribute to your WhatsApp Chat Analyzer tool. You can adapt it as needed, especially with your personal contact details and repository links.

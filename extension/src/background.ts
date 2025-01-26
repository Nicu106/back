let currentData: any = null;

const placeholderData = {
  url: "diez.md",
  summary:
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce convallis neque lacus, id facilisis est auctor et. Cras tempus non tortor dignissim elementum. Donec ut tempor lacus. ",
  relatedArticles: [
    {
      url: "https://diez.md",
      title: "Donald Trump Address to Joint Session of Congress... ",
    },
    {
      url: "https://diez.md",
      title: "Donald Trump Address to Joint Session of Congress... ",
    },
    {
      url: "https://diez.md",
      title: "Donald Trump Address to Joint Session of Congress... ",
    },
  ],
  status: "unreliable",
};

const ENDPOINT = "http://127.0.0.1:8000/analyze_all/"; // Added trailing slash to match curl
const API_KEY = "1fd10517d980ad53ff74945bccb29da0";

// Function to make the fetch request
async function fetchData(url: string) {
  try {
    console.log("Fetching data for URL:", url);
    // Replace with your actual API endpoint
    const response = await fetch(ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-TRUS-API-Key": API_KEY,
      },
      body: JSON.stringify({ contentUri: url, language: "eng" }),
    });
    const data = await response.json();
    const trustLevel = data["trust-level"];
    const summary = data.summary.summary;

    const graph =
      data.graph.length > 0 ? data.graph : placeholderData.relatedArticles;
    currentData = {
      summary: summary,
      relatedArticles: graph,
      status:
        Number(trustLevel["trustLevel"]) <= 50
          ? "bad"
          : Number(trustLevel["trustLevel"]) > 50 &&
            Number(trustLevel["trustLevel"]) <= 85
          ? "unreliable"
          : "good",
    };

    console.log("data", data);
    console.log("Data fetched:", currentData);
  } catch (error) {
    console.error("Fetch error:", error);
    // Fallback to placeholder data if fetch fails
    currentData = placeholderData;
  }
}

// Listen for tab updates - this catches both URL changes and refreshes
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    fetchData(tab.url);
  }
});

// Add message listener for popup to get data
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "GET_DATA") {
    // If no data exists, fetch it for the current tab
    if (!currentData) {
      chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
        if (tabs[0]?.url) {
          await fetchData(tabs[0].url);
          sendResponse(currentData);
        }
      });
      return true; // Keep message channel open for async response
    }
    sendResponse(currentData);
  }
  return true;
});

// Optional: Periodic polling if needed
function polling() {
  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    if (tabs[0]?.url) {
      await fetchData(tabs[0].url);
    }
  });
  setTimeout(polling, 1000 * 30);
}

polling();

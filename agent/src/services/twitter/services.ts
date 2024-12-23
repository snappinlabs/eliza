import axios from "axios";
import * as dotenv from "dotenv";
import { PdfService } from "@ai16z/plugin-node";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";

// Load environment variables from .env file
dotenv.config();

// Define constants
const BEARER_TOKEN = process.env.BEARER_TOKEN;
const BASE_URL = process.env.BASE_URL;

// Ensure BEARER_TOKEN is available
if (!BEARER_TOKEN) {
  throw new Error("BEARER_TOKEN is not defined. Please set it in the .env file.");
}

//Fetch documents for building a custom knowledge base.

export const fetchDocuments = async (): Promise<string[]> => {

  try {
    const pdfFilePath = path.join(path.dirname(fileURLToPath(import.meta.url)), "game.pdf");
    const pdfBuffer = fs.readFileSync(pdfFilePath);
    const pdfService = new PdfService();

    // Convert the PDF buffer to text
    const pdfText = await pdfService.convertPdfToText(pdfBuffer);

    return [pdfText];
  } 
  catch (error) {
    console.error("Error converting PDF to text:", error.message);
    throw new Error("Failed to process the PDF file.");
  }
};

/**
 * Fetch trending tweets from twitter
 * @param query Search query for tweets (default: "sports -is:retweet lang:en").
 * @param maxResults Number of tweets to fetch (default: 10).
 */

  export const fetchSportsTweets = async (
  query: string = "NFL OR NBA OR NHL OR stephcurry OR Lebron  -is:retweet lang:en",
  maxResults: number = 10
): Promise<string[]> => {
  try {
    const url = `${BASE_URL}?query=${encodeURIComponent(query)}&max_results=${maxResults}`;

    // Make API call
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${BEARER_TOKEN}`,
      },
    });

    // Extract tweets and return as an array of strings
    const tweets = response.data.data;
    const texts = tweets.map((item) => item.text);
   // return tweets ? tweets.map((tweet: any) => tweet.text) : [];
    return texts.slice(0, 4).join(' ');
  }

  catch (error: any) {

    console.error("Error fetching tweets:", error.response?.data || error.message);
    throw new Error("Failed to fetch tweets. Please check your network and API credentials.");

  }
}; 
 

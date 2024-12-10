import axios from "axios";
import * as dotenv from "dotenv";
import { PdfService } from "@ai16z/plugin-node";
import * as fs from "fs";

// Load environment variables from .env file
dotenv.config();

// Define constants
const BEARER_TOKEN = process.env.BEARER_TOKEN;
const BASE_URL = "https://api.twitter.com/2/tweets/search/recent";

/**
 * Fetch recent tweets related to sports.
 * @param maxResults Number of tweets to fetch (default: 10)
 */

// this function will get data from documnets for buliding custom knowledge base
export const fetchDocuments = async (): Promise<string[]> => {
    const pdfService = new PdfService();
    const pdfFilePath = "C:/Users/Dell/eliza-1/agent/src/services/twitter/game.pdf";  //a dummy pdf
    const pdfBuffer = fs.readFileSync(pdfFilePath);
    try {
        // Convert the PDF buffer to text
        const pdfText = await pdfService.convertPdfToText(pdfBuffer);

        return [pdfText];
    } catch (error) {
        console.error("Error converting PDF to text:", error);
    }
}


// this function will get trends from twitter
export const fetchSportsTweets = async (maxResults: number = 10): Promise<string[]> => {
    if (!BEARER_TOKEN) {
      throw new Error("Bearer token is missing. Please check your .env file.");
    }

    try {
      const query = "sports -is:retweet lang:en"; // Query to filter tweets
      const url = `${BASE_URL}?query=${encodeURIComponent(query)}&max_results=${maxResults}`;

      // Make API call
      const response = await axios.get(url, {
        headers: {
          Authorization: `Bearer ${BEARER_TOKEN}`,
        },
      });

      // Extract tweets and return as an array of strings
      const tweets = response.data.data;
      if (tweets) {
        return tweets.map((tweet: any) => tweet.text);
      } else {
        return []; // Return an empty array if no tweets are found
      }
    } catch (error: any) {
      console.error("Error fetching tweets:", error.response?.data || error.message);
      throw error;
    }
  };
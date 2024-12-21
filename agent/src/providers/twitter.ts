import { Provider, IAgentRuntime, Memory, State } from "@ai16z/eliza";
import { fetchSportsTweets, fetchDocuments } from "../services/twitter/services.js";


// this is our agent provider for building personality from custom APIs and Knowledgebase
export const tweetsProvider: Provider = {
  get: async (runtime: IAgentRuntime, message: Memory, state?: State) => {
    // Get relevant data using runtime services
    const tweets = await fetchSportsTweets()
   // const documnetsData = (await fetchDocuments()).toString();

    // Format and return context
  //  const data = tweets.concat(documnetsData);

  console.log(tweets);
    return tweets;
  },
  // asdfd
};

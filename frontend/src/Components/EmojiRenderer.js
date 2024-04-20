import React, { useState, useEffect } from "react";
import twemoji from "twemoji";
const EmojiSearcher = ({ input }) => {
  const [emoji, setEmoji] = useState(null);

  useEffect(() => {
    const searchEmoji = () => {
      const searchTerms = input.toLowerCase().split(/\s+/); // Split by whitespace
      let bestMatchScore = 0;
      let bestMatchText = null;

      for (const emojiData of twemoji.parse(input)) {
        let matchScore = 0;

        // Check for exact matches in emoji shortcodes
        if (searchTerms.includes(emojiData.name)) {
          matchScore = 10; // Highest score for exact match
        } else {
          // Check for partial matches in emoji shortcodes (basic implementation)
          for (const term of searchTerms) {
            if (emojiData.name.toLowerCase().includes(term)) {
              matchScore++;
            }
          }
        }

        if (matchScore > bestMatchScore) {
          bestMatchScore = matchScore;
          bestMatchText = emojiData.text;
        }
      }

      setEmoji(bestMatchText);
    };

    if (input) {
      searchEmoji();
    } else {
      setEmoji(null); // Clear emoji if input is empty
    }
  }, [input]);

  useEffect(() => {
    // Initialize twemoji on component mount
    twemoji.parse(document.body);
  }, []);

  return (
    <div>
      {emoji ? (
        <span
          role="img"
          aria-label={emoji}
          title={emoji}
          dangerouslySetInnerHTML={{ __html: twemoji.parse(emoji) }}
        />
      ) : (
        <span>No matching emoji found</span>
      )}
    </div>
  );
};

export default EmojiSearcher;

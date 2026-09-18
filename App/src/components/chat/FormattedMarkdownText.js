import React from 'react';
import { Text, View } from 'react-native';

/**
 * WhatsApp / GFM Markdown Renderer for React Native
 * Formats **bold**, *bold*, _italic_, ~strikethrough~, and bullet/numbered lists cleanly.
 * Uses nested <Text> nodes without flex: 1 to prevent Flexbox bubble collapsing.
 */
export const FormattedMarkdownText = ({ text, style, selectable = true }) => {
  if (!text) return null;

  // Normalize line endings and split into lines
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  let listCounter = 0;

  return (
    <View style={{ width: '100%' }}>
      {lines.map((line, lineIndex) => {
        const trimmed = line.trim();

        // Empty lines create small spacing and reset list counter
        if (!trimmed) {
          listCounter = 0;
          return <View key={lineIndex} style={{ height: 4 }} />;
        }

        // List detection
        const isBullet = trimmed.startsWith('- ') || trimmed.startsWith('• ');
        const isNumbered = /^\d+[\.\)]\s/.test(trimmed);

        let contentText = line;
        let prefix = null;

        if (isBullet) {
          listCounter = 0;
          prefix = '• ';
          contentText = trimmed.substring(2);
        } else if (isNumbered) {
          listCounter++;
          const match = trimmed.match(/^(\d+)([\.\)])\s*(.*)/);
          if (match) {
            const punct = match[2];
            prefix = `${listCounter}${punct} `;
            contentText = match[3];
          }
        } else {
          listCounter = 0;
        }

        return (
          <Text
            key={lineIndex}
            selectable={selectable}
            style={[
              style,
              { marginBottom: lineIndex === lines.length - 1 ? 0 : 3 }
            ]}
          >
            {prefix ? (
              <Text style={[style, { fontWeight: 'bold' }]}>
                {prefix}
              </Text>
            ) : null}
            {parseInlineFormatting(contentText, style)}
          </Text>
        );
      })}
    </View>
  );
};

// Parse inline markup like **bold**, *bold*, _italic_, ~strike~
function parseInlineFormatting(str, baseStyle) {
  if (!str) return null;

  // Split by bold (**text** or *text*), italic (_text_), strike (~text~)
  const regex = /(\*\*[^*]+\*\*|\*[^*]+\*|_[^_]+_|\~[^~]+\~)/g;
  const parts = str.split(regex);

  return parts.map((part, index) => {
    if (!part) return null;

    if (part.startsWith('**') && part.endsWith('**') && part.length > 4) {
      return (
        <Text key={index} style={[baseStyle, { fontWeight: 'bold' }]}>
          {part.slice(2, -2)}
        </Text>
      );
    }
    if (part.startsWith('*') && part.endsWith('*') && part.length > 2) {
      return (
        <Text key={index} style={[baseStyle, { fontWeight: 'bold' }]}>
          {part.slice(1, -1)}
        </Text>
      );
    }
    if (part.startsWith('_') && part.endsWith('_') && part.length > 2) {
      return (
        <Text key={index} style={[baseStyle, { fontStyle: 'italic' }]}>
          {part.slice(1, -1)}
        </Text>
      );
    }
    if (part.startsWith('~') && part.endsWith('~') && part.length > 2) {
      return (
        <Text key={index} style={[baseStyle, { textDecorationLine: 'line-through' }]}>
          {part.slice(1, -1)}
        </Text>
      );
    }

    return <Text key={index} style={baseStyle}>{part}</Text>;
  });
}

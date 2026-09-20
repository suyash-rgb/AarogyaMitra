import React from 'react';

/**
 * Custom WhatsApp Formatted Markdown Renderer
 * Parses:
 *  - *bold* or **bold**
 *  - _italic_
 *  - ~strikethrough~
 *  - Bulleted lists (- or •)
 *  - Numbered lists (1., 2.)
 *  - Links (http/https)
 */
export default function FormattedMarkdownText({ text }) {
  if (!text) return null;

  const lines = text.split('\n');

  return (
    <div className="space-y-1 text-[14.2px] leading-[19px] whitespace-pre-wrap break-words font-sans selection:bg-[#00a884] selection:text-white">
      {lines.map((line, lIdx) => {
        // Bullet list check
        const isBullet = line.trim().startsWith('- ') || line.trim().startsWith('• ');
        const isNumbered = /^\d+\.\s/.test(line.trim());

        let lineContent = line;
        if (isBullet) {
          lineContent = line.trim().replace(/^[-•]\s*/, '');
        }

        const parsedContent = parseInlineStyles(lineContent);

        if (isBullet) {
          return (
            <div key={lIdx} className="flex items-start gap-2 ml-1 my-0.5">
              <span className="text-[#00a884] dark:text-[#00a884] font-bold text-base leading-tight">•</span>
              <div className="flex-1">{parsedContent}</div>
            </div>
          );
        }

        if (isNumbered) {
          const match = line.trim().match(/^(\d+\.)\s*(.*)/);
          return (
            <div key={lIdx} className="flex items-start gap-2 ml-1 my-0.5">
              <span className="font-semibold text-[#00a884] dark:text-[#00a884]">{match ? match[1] : ''}</span>
              <div className="flex-1">{match ? parseInlineStyles(match[2]) : parsedContent}</div>
            </div>
          );
        }

        return <div key={lIdx}>{parsedContent}</div>;
      })}
    </div>
  );
}

function parseInlineStyles(str) {
  if (!str) return '';

  // Regex to tokenise bold (**...** or *...*), italic (_..._), strikethrough (~...~), and URLs
  const tokens = [];
  let remaining = str;

  // Simple sequential parsing for standard WhatsApp markdown
  const parts = [];
  
  // Replace URLs with clickable anchors
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  const segments = str.split(urlRegex);

  return segments.map((seg, i) => {
    if (seg.match(/^https?:\/\//)) {
      return (
        <a
          key={i}
          href={seg}
          target="_blank"
          rel="noopener noreferrer"
          className="text-[#53bdeb] dark:text-[#53bdeb] hover:underline break-all"
        >
          {seg}
        </a>
      );
    }

    // Process bold (*text* or **text**), italic (_text_), strikethrough (~text~)
    return parseTextFormat(seg, i);
  });
}

function parseTextFormat(text, keyPrefix) {
  // Regex pattern for bold (*text*), italic (_text_), strikethrough (~text~)
  const pattern = /(\*{1,2}[^*]+\*{1,2}|_[^_]+_|~[^~]+~)/g;
  const parts = text.split(pattern);

  return parts.map((part, idx) => {
    const key = `${keyPrefix}-${idx}`;
    if (part.startsWith('**') && part.endsWith('**') && part.length > 4) {
      return <strong key={key} className="font-semibold">{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith('*') && part.endsWith('*') && part.length > 2) {
      return <strong key={key} className="font-semibold">{part.slice(1, -1)}</strong>;
    }
    if (part.startsWith('_') && part.endsWith('_') && part.length > 2) {
      return <em key={key} className="italic">{part.slice(1, -1)}</em>;
    }
    if (part.startsWith('~') && part.endsWith('~') && part.length > 2) {
      return <del key={key} className="line-through text-gray-400">{part.slice(1, -1)}</del>;
    }
    return part;
  });
}

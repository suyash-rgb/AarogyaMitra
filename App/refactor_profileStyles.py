import re

with open('src/constants/profileStyles.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Make it a hook
content = content.replace("export const styles = StyleSheet.create({", """import { useTheme } from '../context/ThemeContext';
import { lightColors, darkColors } from './theme';
import { useMemo } from 'react';

export const useStyles = () => {
  const { activeTheme } = useTheme();
  const colors = activeTheme === 'dark' ? darkColors : lightColors;

  return useMemo(() => {
    return StyleSheet.create({""")

content = content.replace("});\n", """    });
  }, [colors]);
};\n""")

# Replace Colors
replacements = [
    (r"'#075E54'", "colors.headerBg"),
    (r"'#E5DDD5'", "colors.background"),
    (r"'#DCF8C6'", "colors.bubbleMe"),
    (r"'#FFFFFF'", "colors.surface"),
    (r"'#fff'", "colors.surface"),
    (r"'#ffffff'", "colors.surface"),
    (r"'#000000'", "colors.text"),
    (r"'#000'", "colors.text"),
    (r"'#111B21'", "colors.text"),
    (r"'#8696a0'", "colors.textSecondary"),
    (r"'#667781'", "colors.textSecondary"),
    (r"'rgba\(255,255,255,0.7\)'", "colors.textSecondary"),
    (r"'#00A884'", "colors.accent"),
    (r"'#E9EDEF'", "colors.border"),
    (r"'#f2f2f2'", "colors.border"),
    (r"'#E2E8F0'", "colors.border"),
    (r"'#EA0038'", "colors.error"),
    (r"'#DC2626'", "colors.dangerBadge"),
    (r"'#0284C7'", "colors.facilityBadge"),
    (r"'#F0F2F5'", "colors.doctorBg"),
    (r"'#E7F7F4'", "colors.accentLight"),
    (r"'rgba\(0,0,0,0.5\)'", "'rgba(0,0,0,0.6)'"),
    (r"'rgba\(0,0,0,0.05\)'", "colors.border"),
    (r"'rgba\(0,0,0,0.15\)'", "colors.border"),
    (r"color:\s*colors\.surface", "color: colors.textInverse"),
]

for old, new in replacements:
    content = re.sub(old, new, content)

with open('src/constants/profileStyles.js', 'w', encoding='utf-8') as f:
    f.write(content)

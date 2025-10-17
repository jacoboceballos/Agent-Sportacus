function formatLLMOutput(text) {
    if (!text) return text;
    
    // Convert markdown-style formatting to HTML
    let formatted = text
        // Headers
        .replace(/^### (.*$)/gm, '<h3>$1</h3>')
        .replace(/^## (.*$)/gm, '<h2>$1</h2>')
        .replace(/^# (.*$)/gm, '<h1>$1</h1>')
        
        // Bold text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        
        // Lists - convert bullet points
        .replace(/^[\*\-\+] (.*$)/gm, '<li>$1</li>')
        .replace(/^(\d+)\. (.*$)/gm, '<li>$1. $2</li>')
        
        // Line breaks and paragraphs
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
    
    // Wrap lists in ul tags
    formatted = formatted.replace(/(<li>.*?<\/li>)/gs, function(match) {
        if (!match.includes('<ul>')) {
            return '<ul>' + match + '</ul>';
        }
        return match;
    });
    
    // Wrap in paragraphs if not already wrapped
    if (!formatted.includes('<p>') && !formatted.includes('<h')) {
        formatted = '<p>' + formatted + '</p>';
    }
    
    return formatted;
}
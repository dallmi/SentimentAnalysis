// Browser DevTools Console Script
// Extract article content from current page

// Step 1: Open the article in your browser
// Step 2: Press F12 to open DevTools
// Step 3: Go to Console tab
// Step 4: Copy and paste this script
// Step 5: Press Enter

(function extractArticleContent() {
    // Get current URL
    const url = window.location.href;

    // Try to find title
    let title = '';
    const titleCandidates = [
        document.querySelector('h1'),
        document.querySelector('title'),
        document.querySelector('[class*="title"]'),
        document.querySelector('[class*="headline"]')
    ];

    for (const candidate of titleCandidates) {
        if (candidate && candidate.textContent.trim()) {
            title = candidate.textContent.trim();
            break;
        }
    }

    // Try to find main content
    let content = '';
    const contentCandidates = [
        document.querySelector('article'),
        document.querySelector('main'),
        document.querySelector('[class*="content"]'),
        document.querySelector('[class*="article"]'),
        document.querySelector('[id*="content"]'),
        document.querySelector('.post-content'),
        document.querySelector('.entry-content')
    ];

    for (const candidate of contentCandidates) {
        if (candidate) {
            // Remove script, style, nav, footer
            const clone = candidate.cloneNode(true);
            clone.querySelectorAll('script, style, nav, footer, header, .comments').forEach(el => el.remove());
            content = clone.textContent.trim();
            if (content.length > 100) { // Make sure we got substantial content
                break;
            }
        }
    }

    // If still no content, try body
    if (!content || content.length < 100) {
        const body = document.body.cloneNode(true);
        body.querySelectorAll('script, style, nav, footer, header, .sidebar, .comments').forEach(el => el.remove());
        content = body.textContent.trim();
    }

    // Clean up whitespace
    content = content.replace(/\s+/g, ' ').trim();

    // Create result object
    const result = {
        url: url,
        title: title,
        content: content
    };

    // Display result
    console.log('=== EXTRACTED ARTICLE ===');
    console.log('URL:', result.url);
    console.log('Title:', result.title);
    console.log('Content Length:', result.content.length, 'characters');
    console.log('\n--- Copy this JSON ---');
    console.log(JSON.stringify(result, null, 2));
    console.log('--- End JSON ---\n');

    // Also copy to clipboard (if browser supports it)
    if (navigator.clipboard) {
        const jsonString = JSON.stringify(result, null, 2);
        navigator.clipboard.writeText(jsonString).then(() => {
            console.log('✓ JSON copied to clipboard!');
        }).catch(() => {
            console.log('⚠ Could not copy to clipboard automatically. Please copy manually from above.');
        });
    }

    return result;
})();

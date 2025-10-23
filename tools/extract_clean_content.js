// Clean Content Extractor - Customizable Version
//
// INSTRUCTIONS:
// 1. Run inspect_page_structure.js first to find your content container
// 2. Update CONTENT_SELECTOR below with the recommended selector
// 3. Run this script to extract clean content

(function extractCleanContent() {
    // ========================================
    // CONFIGURATION - CUSTOMIZE THIS SECTION
    // ========================================

    // Main content selector (update this based on inspect_page_structure.js output)
    const CONTENT_SELECTOR = 'article';  // ← CHANGE THIS to your page's main content container

    // Elements to remove from content (add more if needed)
    const ELEMENTS_TO_REMOVE = [
        'script',
        'style',
        'nav',
        'header',
        'footer',
        '.sidebar',
        '.navigation',
        '.menu',
        '#comment-list',
        '.comments',
        '.comment-section',
        '[id*="comment"]',
        '[class*="comment"]',
        '.social-share',
        '.related-posts',
        '.author-bio',
        'aside',
        '.advertisement',
        '[class*="ad-"]',
        '[id*="ad-"]'
    ];

    // ========================================
    // EXTRACTION LOGIC
    // ========================================

    const url = window.location.href;

    // Extract title
    let title = '';
    const titleCandidates = [
        document.querySelector('h1'),
        document.querySelector('[class*="title"]'),
        document.querySelector('title')
    ];

    for (const candidate of titleCandidates) {
        if (candidate && candidate.textContent.trim()) {
            title = candidate.textContent.trim();
            break;
        }
    }

    // Extract main content
    let content = '';
    const mainElement = document.querySelector(CONTENT_SELECTOR);

    if (mainElement) {
        console.log(`✓ Found content container: ${CONTENT_SELECTOR}`);

        // Clone to avoid modifying the page
        const clone = mainElement.cloneNode(true);

        // Remove unwanted elements
        ELEMENTS_TO_REMOVE.forEach(selector => {
            clone.querySelectorAll(selector).forEach(el => el.remove());
        });

        // Get clean text
        content = clone.textContent.trim();

        // Clean up whitespace
        content = content.replace(/\s+/g, ' ').trim();

        console.log(`✓ Extracted ${content.length} characters`);
    } else {
        console.error(`❌ Content container not found: ${CONTENT_SELECTOR}`);
        console.log('Run inspect_page_structure.js to find the correct selector');
        return null;
    }

    // Extract comments using your existing logic
    const comments = [];
    const commentList = document.querySelector('#comment-list.main');

    if (commentList) {
        const commentElements = commentList.querySelectorAll('li.comment');
        console.log(`✓ Found ${commentElements.length} comments`);

        commentElements.forEach((commentEl) => {
            const contentDiv = commentEl.querySelector('.content');
            const commentText = contentDiv ? contentDiv.textContent.trim() : '';

            const nameDiv = commentEl.querySelector('.name');
            const author = nameDiv ? nameDiv.textContent.trim() : 'Unknown';

            const timeTag = commentEl.querySelector('time');
            const date = timeTag ? (timeTag.getAttribute('data-original') || timeTag.textContent.trim()) : '';

            if (commentText) {
                comments.push({
                    text: commentText,
                    author: author,
                    date: date
                });
            }
        });
    }

    // Create result
    const result = {
        url: url,
        title: title,
        content: content,
        comments: comments
    };

    // Display
    console.log('\n' + '='.repeat(60));
    console.log('EXTRACTED ARTICLE');
    console.log('='.repeat(60));
    console.log('URL:', result.url);
    console.log('Title:', result.title);
    console.log('Content Length:', result.content.length, 'characters');
    console.log('Comments:', result.comments.length);

    if (result.comments.length > 0) {
        console.log('\nFirst comment preview:');
        console.log(`"${result.comments[0].text.substring(0, 100)}..."`);
    }

    console.log('\n--- COPY THIS JSON ---');
    const jsonString = JSON.stringify(result, null, 2);
    console.log(jsonString);
    console.log('--- END JSON ---\n');

    // Copy to clipboard
    if (navigator.clipboard) {
        navigator.clipboard.writeText(jsonString).then(() => {
            console.log('✓ JSON copied to clipboard!');
        }).catch(() => {
            console.log('⚠ Could not copy automatically. Please copy manually.');
        });
    }

    // Show content preview
    console.log('\n' + '='.repeat(60));
    console.log('CONTENT PREVIEW (first 500 chars):');
    console.log('='.repeat(60));
    console.log(content.substring(0, 500) + '...\n');

    return result;
})();

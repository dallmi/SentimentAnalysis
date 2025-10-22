// Browser DevTools Console Script
// Extract article content AND comments from current page

// Step 1: Open the article in your browser
// Step 2: Press F12 to open DevTools
// Step 3: Go to Console tab
// Step 4: Copy and paste this script
// Step 5: Press Enter

(function extractArticleWithComments() {
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

    // Try to find main content (EXCLUDING comments section)
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
            // Remove script, style, nav, footer, comments
            const clone = candidate.cloneNode(true);
            clone.querySelectorAll('script, style, nav, footer, header, .comments, .comment-section, [class*="comment"], [id*="comment"]').forEach(el => el.remove());
            content = clone.textContent.trim();
            if (content.length > 100) { // Make sure we got substantial content
                break;
            }
        }
    }

    // If still no content, try body (excluding comments)
    if (!content || content.length < 100) {
        const body = document.body.cloneNode(true);
        body.querySelectorAll('script, style, nav, footer, header, .sidebar, .comments, .comment-section, [class*="comment"], [id*="comment"]').forEach(el => el.remove());
        content = body.textContent.trim();
    }

    // Clean up whitespace
    content = content.replace(/\s+/g, ' ').trim();

    // ========================================
    // EXTRACT COMMENTS
    // ========================================

    const comments = [];

    // Try different common comment section selectors
    const commentSectionCandidates = [
        // Generic selectors
        '.comments',
        '.comment-section',
        '.comments-section',
        '#comments',
        '#comment-section',
        '[class*="comment"]',
        '[id*="comment"]',

        // SharePoint specific
        '.ms-commentsList',
        '.ms-comments',
        '[class*="Comment"]',

        // Common CMS patterns
        '.discussion',
        '.feedback',
        '.user-comments',
        'div[data-comments]',

        // Try finding by text content
        ...Array.from(document.querySelectorAll('h2, h3, h4')).filter(h =>
            /comment|kommentar|feedback|discussion/i.test(h.textContent)
        ).map(h => h.parentElement)
    ];

    let commentSection = null;
    for (const selector of commentSectionCandidates) {
        if (typeof selector === 'string') {
            commentSection = document.querySelector(selector);
        } else {
            commentSection = selector;
        }

        if (commentSection) {
            console.log('Found comment section:', commentSection);
            break;
        }
    }

    if (commentSection) {
        // Try to extract individual comments
        const commentCandidates = [
            '.comment',
            '.comment-item',
            '.user-comment',
            '[class*="comment-"]',
            '.ms-commentItem',
            'li[class*="comment"]',
            'div[class*="comment"]'
        ];

        let commentElements = [];
        for (const selector of commentCandidates) {
            commentElements = commentSection.querySelectorAll(selector);
            if (commentElements.length > 0) {
                console.log(`Found ${commentElements.length} comments with selector: ${selector}`);
                break;
            }
        }

        // Extract comment data
        commentElements.forEach((commentEl, index) => {
            // Try to find comment text
            let commentText = '';
            const textCandidates = [
                commentEl.querySelector('.comment-text'),
                commentEl.querySelector('.comment-content'),
                commentEl.querySelector('.comment-body'),
                commentEl.querySelector('p'),
                commentEl
            ];

            for (const textEl of textCandidates) {
                if (textEl) {
                    const clone = textEl.cloneNode(true);
                    // Remove nested metadata (author, date, etc.)
                    clone.querySelectorAll('.author, .date, .time, .meta, button, a').forEach(el => el.remove());
                    commentText = clone.textContent.trim();
                    if (commentText.length > 10) {
                        break;
                    }
                }
            }

            // Try to find author
            let author = '';
            const authorCandidates = [
                commentEl.querySelector('.comment-author'),
                commentEl.querySelector('.author'),
                commentEl.querySelector('.user-name'),
                commentEl.querySelector('[class*="author"]')
            ];

            for (const authorEl of authorCandidates) {
                if (authorEl) {
                    author = authorEl.textContent.trim();
                    break;
                }
            }

            // Try to find date
            let date = '';
            const dateCandidates = [
                commentEl.querySelector('.comment-date'),
                commentEl.querySelector('.date'),
                commentEl.querySelector('time'),
                commentEl.querySelector('[class*="date"]')
            ];

            for (const dateEl of dateCandidates) {
                if (dateEl) {
                    date = dateEl.textContent.trim();
                    break;
                }
            }

            if (commentText) {
                comments.push({
                    text: commentText,
                    author: author || 'Unknown',
                    date: date || ''
                });
            }
        });

        console.log(`✓ Extracted ${comments.length} comments`);
    } else {
        console.log('⚠ No comment section found. You may need to inspect the page manually.');
        console.log('Try running this in the console to find comments:');
        console.log('  document.querySelectorAll("*")');
        console.log('  Then look for elements that contain comment text');
    }

    // Create result object
    const result = {
        url: url,
        title: title,
        content: content,
        comments: comments
    };

    // Display result
    console.log('\n=== EXTRACTED ARTICLE WITH COMMENTS ===');
    console.log('URL:', result.url);
    console.log('Title:', result.title);
    console.log('Content Length:', result.content.length, 'characters');
    console.log('Comments Found:', result.comments.length);

    if (result.comments.length > 0) {
        console.log('\nFirst few comments:');
        result.comments.slice(0, 3).forEach((comment, i) => {
            console.log(`  ${i+1}. ${comment.author}: ${comment.text.substring(0, 100)}...`);
        });
    }

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

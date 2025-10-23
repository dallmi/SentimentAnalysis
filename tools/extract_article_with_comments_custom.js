// Browser DevTools Console Script - CUSTOM VERSION
// Extract article content AND comments from current page
// Optimized for your specific SharePoint/Intranet structure

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
            clone.querySelectorAll('script, style, nav, footer, header, .comments, #comment-list, [id*="comment"]').forEach(el => el.remove());
            content = clone.textContent.trim();
            if (content.length > 100) { // Make sure we got substantial content
                break;
            }
        }
    }

    // If still no content, try body (excluding comments)
    if (!content || content.length < 100) {
        const body = document.body.cloneNode(true);
        body.querySelectorAll('script, style, nav, footer, header, .sidebar, #comment-list, [id*="comment"]').forEach(el => el.remove());
        content = body.textContent.trim();
    }

    // Clean up whitespace
    content = content.replace(/\s+/g, ' ').trim();

    // ========================================
    // EXTRACT COMMENTS - CUSTOM FOR YOUR SITE
    // ========================================

    const comments = [];

    // Find the comment list using your specific structure
    const commentList = document.querySelector('#comment-list.main');

    if (commentList) {
        console.log('✓ Found comment list!');

        // Get all <li> elements with class "comment"
        const commentElements = commentList.querySelectorAll('li.comment');
        console.log(`✓ Found ${commentElements.length} comment elements`);

        commentElements.forEach((commentEl, index) => {
            try {
                // Extract comment text from <div class="content">
                const contentDiv = commentEl.querySelector('.content');
                const commentText = contentDiv ? contentDiv.textContent.trim() : '';

                // Extract author from <div class="name">
                const nameDiv = commentEl.querySelector('.name');
                const author = nameDiv ? nameDiv.textContent.trim() : 'Unknown';

                // Extract date from <time> tag
                const timeTag = commentEl.querySelector('time');
                let date = '';
                if (timeTag) {
                    // Try data-original attribute first (full timestamp)
                    date = timeTag.getAttribute('data-original') || timeTag.textContent.trim();
                }

                // Only add if we have actual comment text
                if (commentText && commentText.length > 0) {
                    comments.push({
                        text: commentText,
                        author: author,
                        date: date
                    });
                }
            } catch (error) {
                console.warn(`⚠ Error extracting comment ${index + 1}:`, error);
            }
        });

        console.log(`✓ Successfully extracted ${comments.length} comments`);
    } else {
        console.log('⚠ No comment list found with id="comment-list"');

        // Try alternative: look for any <ul> or <ol> containing comment <li> elements
        const alternativeComments = document.querySelectorAll('li.comment');
        if (alternativeComments.length > 0) {
            console.log(`✓ Found ${alternativeComments.length} comment elements (alternative method)`);

            alternativeComments.forEach((commentEl, index) => {
                try {
                    const contentDiv = commentEl.querySelector('.content');
                    const commentText = contentDiv ? contentDiv.textContent.trim() : '';

                    const nameDiv = commentEl.querySelector('.name');
                    const author = nameDiv ? nameDiv.textContent.trim() : 'Unknown';

                    const timeTag = commentEl.querySelector('time');
                    const date = timeTag ? (timeTag.getAttribute('data-original') || timeTag.textContent.trim()) : '';

                    if (commentText && commentText.length > 0) {
                        comments.push({
                            text: commentText,
                            author: author,
                            date: date
                        });
                    }
                } catch (error) {
                    console.warn(`⚠ Error extracting comment ${index + 1}:`, error);
                }
            });

            console.log(`✓ Successfully extracted ${comments.length} comments (alternative method)`);
        }
    }

    // Also extract nested/child comments if they exist
    const childComments = document.querySelectorAll('ul.child-comments li.comment');
    if (childComments.length > 0) {
        console.log(`✓ Found ${childComments.length} child/nested comments`);

        childComments.forEach((commentEl, index) => {
            try {
                const contentDiv = commentEl.querySelector('.content');
                const commentText = contentDiv ? contentDiv.textContent.trim() : '';

                const nameDiv = commentEl.querySelector('.name');
                const author = nameDiv ? nameDiv.textContent.trim() : 'Unknown';

                const timeTag = commentEl.querySelector('time');
                const date = timeTag ? (timeTag.getAttribute('data-original') || timeTag.textContent.trim()) : '';

                if (commentText && commentText.length > 0) {
                    comments.push({
                        text: commentText,
                        author: author,
                        date: date,
                        type: 'reply'  // Mark as a reply/nested comment
                    });
                }
            } catch (error) {
                console.warn(`⚠ Error extracting child comment ${index + 1}:`, error);
            }
        });
    }

    // Create result object
    const result = {
        url: url,
        title: title,
        content: content,
        comments: comments
    };

    // Display result
    console.log('\n' + '='.repeat(60));
    console.log('EXTRACTED ARTICLE WITH COMMENTS');
    console.log('='.repeat(60));
    console.log('URL:', result.url);
    console.log('Title:', result.title);
    console.log('Content Length:', result.content.length, 'characters');
    console.log('Comments Found:', result.comments.length);

    if (result.comments.length > 0) {
        console.log('\n--- First 3 Comments Preview ---');
        result.comments.slice(0, 3).forEach((comment, i) => {
            console.log(`\n${i+1}. ${comment.author} (${comment.date})`);
            console.log(`   "${comment.text.substring(0, 100)}${comment.text.length > 100 ? '...' : ''}"`);
        });
    }

    console.log('\n' + '='.repeat(60));
    console.log('JSON OUTPUT (Copy this)');
    console.log('='.repeat(60));
    const jsonString = JSON.stringify(result, null, 2);
    console.log(jsonString);
    console.log('='.repeat(60));

    // Copy to clipboard (if browser supports it)
    if (navigator.clipboard) {
        navigator.clipboard.writeText(jsonString).then(() => {
            console.log('\n✓ JSON copied to clipboard!');
            console.log('You can now paste it into your extracted_articles.json file');
        }).catch(() => {
            console.log('\n⚠ Could not copy to clipboard automatically.');
            console.log('Please select and copy the JSON manually from above.');
        });
    }

    return result;
})();

// Browser DevTools Console Script - HIERARCHICAL VERSION
// Extract article content AND comments WITH PROPER ORDERING
// Preserves comment hierarchy: Comment 1, Reply 1, Comment 2, Reply 2, etc.

// Step 1: Open the article in your browser
// Step 2: Press F12 to open DevTools
// Step 3: Go to Console tab
// Step 4: Copy and paste this script
// Step 5: Press Enter

(function extractArticleWithCommentsHierarchical() {
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
    // EXTRACT COMMENTS - HIERARCHICAL ORDER
    // ========================================

    const comments = [];

    // Helper function to extract comment data
    function extractCommentData(commentEl, isReply = false) {
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

            // Only return if we have actual comment text
            if (commentText && commentText.length > 0) {
                const comment = {
                    text: commentText,
                    author: author,
                    date: date
                };

                // Mark as reply if it's a nested comment
                if (isReply) {
                    comment.type = 'reply';
                }

                return comment;
            }
        } catch (error) {
            console.warn(`⚠ Error extracting comment:`, error);
        }
        return null;
    }

    // Find the comment list using your specific structure
    const commentList = document.querySelector('#comment-list.main');

    if (commentList) {
        console.log('✓ Found comment list!');

        // Get all top-level <li> elements with class "comment" (direct children only)
        // This ensures we don't accidentally get nested comments twice
        const topLevelComments = commentList.querySelectorAll(':scope > li.comment');
        console.log(`✓ Found ${topLevelComments.length} top-level comment elements`);

        topLevelComments.forEach((commentEl, index) => {
            // Extract the main comment
            const mainComment = extractCommentData(commentEl, false);
            if (mainComment) {
                comments.push(mainComment);
            }

            // Now look for child comments WITHIN this comment element
            const childCommentList = commentEl.querySelector('ul.child-comments');
            if (childCommentList) {
                const childComments = childCommentList.querySelectorAll('li.comment');
                console.log(`  └─ Found ${childComments.length} replies for comment ${index + 1}`);

                childComments.forEach(childEl => {
                    const childComment = extractCommentData(childEl, true);
                    if (childComment) {
                        comments.push(childComment);
                    }
                });
            }
        });

        console.log(`✓ Successfully extracted ${comments.length} comments (hierarchical order)`);
    } else {
        console.log('⚠ No comment list found with id="comment-list"');

        // Fallback: Try to find comments and preserve order as best as possible
        const allComments = document.querySelectorAll('li.comment');
        if (allComments.length > 0) {
            console.log(`✓ Found ${allComments.length} comment elements (alternative method)`);

            allComments.forEach((commentEl, index) => {
                // Check if this is a nested comment by looking at parent structure
                const isNested = commentEl.closest('ul.child-comments') !== null;

                const comment = extractCommentData(commentEl, isNested);
                if (comment) {
                    comments.push(comment);
                }
            });

            console.log(`✓ Successfully extracted ${comments.length} comments (alternative method)`);
        }
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
    console.log('EXTRACTED ARTICLE WITH COMMENTS (HIERARCHICAL)');
    console.log('='.repeat(60));
    console.log('URL:', result.url);
    console.log('Title:', result.title);
    console.log('Content Length:', result.content.length, 'characters');
    console.log('Comments Found:', result.comments.length);

    // Show comment structure
    if (result.comments.length > 0) {
        console.log('\n--- Comment Structure Preview ---');
        result.comments.forEach((comment, i) => {
            const prefix = comment.type === 'reply' ? '  └─ Reply' : `${i+1}. Comment`;
            const preview = comment.text.substring(0, 80);
            console.log(`${prefix}: ${comment.author} - "${preview}${comment.text.length > 80 ? '...' : ''}"`);
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

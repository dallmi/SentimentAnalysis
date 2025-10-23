// Page Structure Inspector
// Run this in browser console to find the main content container

(function inspectPageStructure() {
    console.log('='.repeat(60));
    console.log('PAGE STRUCTURE ANALYSIS');
    console.log('='.repeat(60));

    // 1. Find potential article containers
    console.log('\n1. ARTICLE CONTAINERS:');
    const articleContainers = [
        { selector: 'article', element: document.querySelector('article') },
        { selector: 'main', element: document.querySelector('main') },
        { selector: '[role="main"]', element: document.querySelector('[role="main"]') },
        { selector: '.article', element: document.querySelector('.article') },
        { selector: '.post', element: document.querySelector('.post') },
        { selector: '[class*="article"]', element: document.querySelector('[class*="article"]') },
        { selector: '[class*="post"]', element: document.querySelector('[class*="post"]') },
        { selector: '[id*="article"]', element: document.querySelector('[id*="article"]') },
        { selector: '[id*="post"]', element: document.querySelector('[id*="post"]') },
        { selector: '[id*="content"]', element: document.querySelector('[id*="content"]') }
    ];

    articleContainers.forEach(({ selector, element }) => {
        if (element) {
            const textLength = element.textContent.trim().length;
            const childCount = element.children.length;
            console.log(`✓ Found: ${selector}`);
            console.log(`  Text length: ${textLength} chars`);
            console.log(`  Children: ${childCount}`);
            console.log(`  Classes: ${element.className}`);
            console.log(`  ID: ${element.id}`);

            // Show first 100 chars
            const preview = element.textContent.trim().substring(0, 100);
            console.log(`  Preview: "${preview}..."`);
            console.log('');
        }
    });

    // 2. Find title
    console.log('\n2. TITLE:');
    const titleCandidates = [
        { selector: 'h1', element: document.querySelector('h1') },
        { selector: '[class*="title"]', element: document.querySelector('[class*="title"]') },
        { selector: 'title', element: document.querySelector('title') }
    ];

    titleCandidates.forEach(({ selector, element }) => {
        if (element) {
            console.log(`✓ ${selector}: "${element.textContent.trim()}"`);
        }
    });

    // 3. Find comment section
    console.log('\n3. COMMENT SECTION:');
    const commentSectionFound = document.querySelector('#comment-list.main');
    if (commentSectionFound) {
        const commentCount = commentSectionFound.querySelectorAll('li.comment').length;
        console.log(`✓ Comment section found: #comment-list.main`);
        console.log(`  Comments: ${commentCount}`);
    } else {
        console.log('⚠ Comment section not found (expected #comment-list.main)');
    }

    // 4. Find what to EXCLUDE
    console.log('\n4. ELEMENTS TO EXCLUDE:');
    const excludeElements = [
        { name: 'Navigation', selector: 'nav', count: document.querySelectorAll('nav').length },
        { name: 'Header', selector: 'header', count: document.querySelectorAll('header').length },
        { name: 'Footer', selector: 'footer', count: document.querySelectorAll('footer').length },
        { name: 'Sidebar', selector: '.sidebar', count: document.querySelectorAll('.sidebar').length },
        { name: 'Comments', selector: '#comment-list', count: document.querySelectorAll('#comment-list').length },
        { name: 'Ads', selector: '[class*="ad"]', count: document.querySelectorAll('[class*="ad"]').length }
    ];

    excludeElements.forEach(({ name, selector, count }) => {
        if (count > 0) {
            console.log(`✓ ${name} (${selector}): ${count} found`);
        }
    });

    // 5. All unique IDs and classes
    console.log('\n5. UNIQUE IDs on page:');
    const allElements = document.querySelectorAll('[id]');
    const uniqueIds = new Set();
    allElements.forEach(el => {
        if (el.id) uniqueIds.add(el.id);
    });
    console.log(Array.from(uniqueIds).slice(0, 20).join(', '));

    console.log('\n6. COMMON CLASSES:');
    const allClasses = new Set();
    document.querySelectorAll('*').forEach(el => {
        if (el.className && typeof el.className === 'string') {
            el.className.split(' ').forEach(cls => {
                if (cls) allClasses.add(cls);
            });
        }
    });
    const sortedClasses = Array.from(allClasses).sort();
    console.log('First 30 classes:', sortedClasses.slice(0, 30).join(', '));

    // 7. RECOMMENDATION
    console.log('\n' + '='.repeat(60));
    console.log('RECOMMENDATION:');
    console.log('='.repeat(60));

    // Find best content container
    let bestContainer = null;
    let bestScore = 0;

    articleContainers.forEach(({ selector, element }) => {
        if (element) {
            const clone = element.cloneNode(true);

            // Remove unwanted elements
            clone.querySelectorAll('nav, footer, header, .sidebar, #comment-list, [id*="comment"], script, style').forEach(el => el.remove());

            const cleanTextLength = clone.textContent.trim().length;
            const score = cleanTextLength;

            if (score > bestScore && cleanTextLength > 200) {
                bestScore = score;
                bestContainer = { selector, element, cleanTextLength };
            }
        }
    });

    if (bestContainer) {
        console.log(`Best container: ${bestContainer.selector}`);
        console.log(`Clean text length: ${bestContainer.cleanTextLength} chars`);
        console.log(`\nUse this selector in your extraction script:`);
        console.log(`const mainContent = document.querySelector('${bestContainer.selector}');`);

        // Show preview
        const clone = bestContainer.element.cloneNode(true);
        clone.querySelectorAll('nav, footer, header, .sidebar, #comment-list, [id*="comment"], script, style').forEach(el => el.remove());
        const preview = clone.textContent.trim().substring(0, 300);
        console.log(`\nContent preview:\n"${preview}..."`);
    } else {
        console.log('⚠ Could not find suitable content container');
        console.log('Try inspecting the page manually:');
        console.log('1. Right-click on article text');
        console.log('2. Select "Inspect"');
        console.log('3. Look for the parent container with class/id');
    }

    console.log('\n' + '='.repeat(60));

})();

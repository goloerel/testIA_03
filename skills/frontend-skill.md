Frontend Development Standards
CSS Methodology

    Naming Convention: Use only single hyphens for class names (e.g., card-header-title).

    Symbol Restriction: NEVER use underscores _ or double symbols like -- or __.

    Organization: Prioritize a single main.css for all general styles to keep the project footprint small. 

JavaScript Patterns

    Data Flow: Pass data explicitly as arguments between functions.

    State Management: NEVER rely on a global "God" store object; keep state localized to the function scope where possible.

    Modularity: Use ES6 modules to organize code into logical units (e.g., api.js, ui.js). 

UI Requirements

    Frameworks: NEVER use React, Vue, or any other framework; stay strictly within Vanilla JS.

    Accessibility: Ensure all interactive elements have proper ARIA labels and keyboard focus states.
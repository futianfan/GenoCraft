const gulp = require("gulp");
const gap = require("gulp-append-prepend");

gulp.task("licenses", async function () {
    // this is to add Creative Tim licenses in the production mode for the minified js
    gulp
        .src("build/static/js/*chunk.js", {base: "./"})
        .pipe(
            gap.prependText(`/*!

=========================================================
* GenoCraft - v1.0 by Minjie Shen
=========================================================

* Github Page: https://github.com/futianfan/GenoCraft
* Copyright 2023
* Licensed under MIT:
Copyright (c) 2023 - present GenoCraft (https://github.com/futianfan/GenoCraft)
Copyright (c) 2019 - present CodedThemes (https://codedthemes.com/)
Copyright (c) 2021 - present Creative Tim (https://www.creative-tim.com?ref=nr-license)
Copyright (c) 2019 - present AppSeed (https://appseed.us/)
Copyright (c) 2020 - present tsParticles (https://github.com/tsparticles/tsparticles)

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/`)
        )
        .pipe(gulp.dest("./", {overwrite: true}));

    // this is to add Creative Tim licenses in the production mode for the minified html
    gulp
        .src("build/index.html", {base: "./"})
        .pipe(
            gap.prependText(`<!--

=========================================================
* GenoCraft - v1.0 by Minjie Shen
=========================================================

* Github Page: https://github.com/futianfan/GenoCraft
* Copyright 2023
* Licensed under MIT:
Copyright (c) 2023 - present GenoCraft (https://github.com/futianfan/GenoCraft)
Copyright (c) 2019 - present CodedThemes (https://codedthemes.com/)
Copyright (c) 2021 - present Creative Tim (https://www.creative-tim.com?ref=nr-license)
Copyright (c) 2019 - present AppSeed (https://appseed.us/)
Copyright (c) 2020 - present tsParticles (https://github.com/tsparticles/tsparticles)

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

-->`)
        )
        .pipe(gulp.dest("./", {overwrite: true}));

    // this is to add Creative Tim licenses in the production mode for the minified css
    gulp
        .src("build/static/css/*chunk.css", {base: "./"})
        .pipe(
            gap.prependText(`/*!

=========================================================
* GenoCraft - v1.0 by Minjie Shen
=========================================================

* Github Page: https://github.com/futianfan/GenoCraft
* Copyright 2023
* Licensed under MIT:
Copyright (c) 2023 - present GenoCraft (https://github.com/futianfan/GenoCraft)
Copyright (c) 2019 - present CodedThemes (https://codedthemes.com/)
Copyright (c) 2021 - present Creative Tim (https://www.creative-tim.com?ref=nr-license)
Copyright (c) 2019 - present AppSeed (https://appseed.us/)
Copyright (c) 2020 - present tsParticles (https://github.com/tsparticles/tsparticles)

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/`)
        )
        .pipe(gulp.dest("./", {overwrite: true}));

});
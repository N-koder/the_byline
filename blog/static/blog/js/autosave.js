(function () {
    let articleId = null;
    let saveTimer;

    function initAutosave() {
        var $ = django.jQuery;
        console.log("Autosave script initialized");

        function showLastSaved() {
            if (!$("#last-saved").length) {
                $("#content h1").after('<p id="last-saved" style="color:green; font-size:12px;">Draft saved just now</p>');
            }
            const msg = "Last saved at " + new Date().toLocaleTimeString();
            $("#last-saved").text(msg);
            console.log(msg);
        }

        function autosave() {
            console.log("Autosave triggered");

            let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            if (!csrfToken) {
                console.error("CSRF token not found");
                return;
            }

            if (!articleId) {
                const match = window.location.pathname.match(/\/article\/(\d+)\/change\//);
                articleId = match ? match[1] : "";
            }

            let title = $("#id_title").val() || "";
            let slug = $("#id_slug").val() || "";
            let summary = tinymce.get("id_summary")?.getContent() || "";
            let body = tinymce.get("id_body")?.getContent() || "";
            let author = $("#id_author").val() || "";
            let tags = $("#id_tags").val() || "";

            // console.log("Autosave data:", { articleId, title, slug, summary: summary.slice(0, 50) + "...", body: body.slice(0, 50) + "...", author, tags });

            $.ajax({
                url: "/blog/autosave/",
                method: "POST",
                data: {
                    id: articleId,
                    title,
                    slug,
                    summary,
                    body,
                    author,
                    tags,
                    csrfmiddlewaretoken: csrfToken
                },
                beforeSend: function () {
                    console.log("Sending AJAX request to /blog/autosave/");
                },
                success: function (res) {
                    // console.log("Autosave response:", res);
                    showLastSaved();

                    if (res.id && !articleId) {
                        articleId = res.id;
                        if (!$("#id_articleId").length) {
                            $("<input>", {
                                type: "hidden",
                                id: "id_articleId",
                                name: "articleId",
                                value: articleId
                            }).appendTo("form");
                        } else {
                            $("#id_articleId").val(articleId);
                        }
                        // console.log("New Article ID assigned:", articleId);
                    }
                },
                error: function (xhr, status, error) {
                    console.error("Autosave failed:", error, xhr.responseText);
                },
                complete: function () {
                    console.log("Autosave AJAX request completed");
                }
            });
        }

        function triggerAutosave() {
            clearTimeout(saveTimer);
            saveTimer = setTimeout(autosave, 1000);
            console.log("Autosave scheduled in 1s");
        }

        // Normal fields
        $("#id_title, #id_author, #id_tags").on("input", triggerAutosave);

        // TinyMCE fields
        const attachTinyMCEListeners = () => {
            // console.log("attachTinyMCEListeners called");

            if (typeof tinymce === "undefined") {
                // console.log("TinyMCE is undefined");
                return;
            }

            // Correct way to access TinyMCE editors
            const editors = tinymce.get(); // This returns an array of all editors
            // console.log("TinyMCE editors found:", editors);

            if (!editors || editors.length === 0) {
                // console.log("No TinyMCE editors found");
                return;
            }

            // Iterate all existing editors and attach listener
            editors.forEach((editor, index) => {
                // console.log("Processing editor:", editor.id);

                if (editor && !editor.hasAutosaveListener) {
                    // Try both 'input' and 'change' events for compatibility
                    editor.on('input', triggerAutosave);
                    editor.on('change', triggerAutosave);
                    editor.on('keyup', triggerAutosave); // Additional event for more responsive autosave
                    editor.hasAutosaveListener = true;
                    // console.log("Autosave listener attached to editor:", editor.id);
                } else {
                    console.log("Skipping editor:", editor.id, "already has listener or is invalid");
                }
            });
        }

        let attempts = 0;
        const maxAttempts = 100; // Try for 10 seconds (100ms * 100)
        const tinymceCheck = setInterval(() => {
            attempts++;
            // console.log("Checking for TinyMCE editors, attempt:", attempts);

            if (typeof tinymce !== "undefined") {
                const editors = tinymce.get();
                // console.log("TinyMCE found, editors:", editors);

                if (editors && editors.length > 0) {
                    attachTinyMCEListeners();
                    clearInterval(tinymceCheck);
                    // console.log("TinyMCE editors ready, listeners attached");
                } else if (attempts >= maxAttempts) {
                    clearInterval(tinymceCheck);
                    // console.log("TinyMCE editors not found after maximum attempts");
                }
            } else if (attempts >= maxAttempts) {
                clearInterval(tinymceCheck);
                // console.log("TinyMCE not found after maximum attempts");
            }
        }, 100);

        window.addEventListener('beforeunload', () => {
            console.log("Page unloading, sending final autosave via sendBeacon");
            const params = new URLSearchParams({
                id: articleId,
                title: $("#id_title").val() || "",
                slug: $("#id_slug").val() || "",
                summary: tinymce.get("id_summary")?.getContent() || "",
                body: tinymce.get("id_body")?.getContent() || "",
                author: $("#id_author").val() || "",
                tags: $("#id_tags").val() || "",
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            });
            navigator.sendBeacon("/blog/autosave/", params);
        });
    }

    function checkDjango() {
        if (typeof django !== "undefined" && typeof django.jQuery !== "undefined") {
            console.log("Django jQuery detected, initializing autosave");
            initAutosave();
        } else {
            setTimeout(checkDjango, 100);
        }
    }

    checkDjango();
})();

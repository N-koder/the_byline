(function () {
    let podcastId = null;
    let saveTimer;

    function initPodcastAutosave() {
        var $ = django.jQuery;
        console.log("Podcast autosave script initialized");

        function showLastSaved() {
            if (!$("#last-saved").length) {
                $("#content h1").after('<p id="last-saved" style="color:green; font-size:12px;">Draft saved just now</p>');
            }
            const msg = "Last saved at " + new Date().toLocaleTimeString();
            $("#last-saved").text(msg);
            console.log(msg);
        }

        function autosave() {
            console.log("Podcast autosave triggered");

            let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            if (!csrfToken) {
                console.error("CSRF token not found");
                return;
            }

            if (!podcastId) {
                const match = window.location.pathname.match(/\/admin\/blog\/podcast\/(\d+)\/change\//);
                podcastId = match ? match[1] : "";
            }

            let title = $("#id_title").val() || "";
            let slug = $("#id_slug").val() || "";
            let description = tinymce.get("id_description")?.getContent() || "";;
            // let author = $("#id_author").val() || "";
            let audio_link = $("#id_audio_link").val() || "";
            let youtube_embed = $("#id_youtube_embed").val() || "";
            let transcript = tinymce.get("id_transcript")?.getContent() || "";

            console.log("Podcast autosave data:", {
                podcastId,
                title,
                slug,
                description: description.slice(0, 50) + "...",
                audio_link,
                youtube_embed,
                transcript: transcript.slice(0, 50) + "...",
                // author
            });

            $.ajax({
                url: "/admin/blog/podcast/autosave-draft/",
                method: "POST",
                data: {
                    id: podcastId,
                    title,
                    slug,
                    description,
                    // author,
                    audio_link,
                    youtube_embed,
                    transcript,
                    csrfmiddlewaretoken: csrfToken
                },
                beforeSend: function () {
                    console.log("Sending AJAX request to /blog/admin/blog/podcast/autosave-draft/");
                },
                success: function (res) {
                    console.log("Podcast autosave response:", res);
                    showLastSaved();

                    if (res.id && !podcastId) {
                        podcastId = res.id;
                        if (!$("#id_podcastId").length) {
                            $("<input>", {
                                type: "hidden",
                                id: "id_podcastId",
                                name: "podcastId",
                                value: podcastId
                            }).appendTo("form");
                        } else {
                            $("#id_podcastId").val(podcastId);
                        }
                        console.log("New Podcast ID assigned:", podcastId);
                    }
                },
                error: function (xhr, status, error) {
                    console.error("Podcast autosave failed:", error, xhr.responseText);
                },
                complete: function () {
                    console.log("Podcast autosave AJAX request completed");
                }
            });
        }

        function triggerAutosave() {
            clearTimeout(saveTimer);
            saveTimer = setTimeout(autosave, 1000);
            console.log("Podcast autosave scheduled in 1s");
        }

        // Normal fields
        $("#id_title, #id_slug, #id_description, #id_author, #id_audio_link, #id_youtube_embed").on("input", triggerAutosave);

        // TinyMCE fields
        const attachTinyMCEListeners = () => {
            console.log("Attaching TinyMCE listeners for podcast");

            if (typeof tinymce === "undefined") {
                console.log("TinyMCE is undefined");
                return;
            }

            const editors = tinymce.get();
            console.log("TinyMCE editors found:", editors);

            if (!editors || editors.length === 0) {
                console.log("No TinyMCE editors found");
                return;
            }

            editors.forEach((editor, index) => {
                console.log("Processing podcast editor:", editor.id);

                if (editor && !editor.hasAutosaveListener) {
                    editor.on('input', triggerAutosave);
                    editor.on('change', triggerAutosave);
                    editor.on('keyup', triggerAutosave);
                    editor.hasAutosaveListener = true;
                    console.log("Autosave listener attached to podcast editor:", editor.id);
                } else {
                    console.log("Skipping podcast editor:", editor.id, "already has listener or is invalid");
                }
            });
        }

        let attempts = 0;
        const maxAttempts = 100;
        const tinymceCheck = setInterval(() => {
            attempts++;
            console.log("Checking for TinyMCE editors (podcast), attempt:", attempts);

            if (typeof tinymce !== "undefined") {
                const editors = tinymce.get();
                console.log("TinyMCE found for podcast, editors:", editors);

                if (editors && editors.length > 0) {
                    attachTinyMCEListeners();
                    clearInterval(tinymceCheck);
                    console.log("TinyMCE editors ready for podcast, listeners attached");
                } else if (attempts >= maxAttempts) {
                    clearInterval(tinymceCheck);
                    console.log("TinyMCE editors not found after maximum attempts (podcast)");
                }
            } else if (attempts >= maxAttempts) {
                clearInterval(tinymceCheck);
                console.log("TinyMCE not found after maximum attempts (podcast)");
            }
        }, 100);

        window.addEventListener('beforeunload', () => {
            console.log("Page unloading, sending final podcast autosave via sendBeacon");
            const params = new URLSearchParams({
                id: podcastId,
                title: $("#id_title").val() || "",
                slug: $("#id_slug").val() || "",
                description: $("#id_description").val() || "",
                author: $("#id_author").val() || "",
                audio_link: $("#id_audio_link").val() || "",
                youtube_embed: $("#id_youtube_embed").val() || "",
                transcript: tinymce.get("id_transcript")?.getContent() || "",
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            });
            navigator.sendBeacon("/blog/admin/blog/podcast/autosave-draft/", params);
        });
    }

    function checkDjango() {
        if (typeof django !== "undefined" && typeof django.jQuery !== "undefined") {
            console.log("Django jQuery detected, initializing podcast autosave");
            initPodcastAutosave();
        } else {
            setTimeout(checkDjango, 100);
        }
    }

    checkDjango();
})();

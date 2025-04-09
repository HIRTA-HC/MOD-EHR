
import { getUserSession, togglePasswordVisibility } from "./common";
import { signIn } from "aws-amplify/auth";


$(document).ready(async function () {
    $("#login").click(async function () {
        const username = $("#email").val();
        const password = $("#password").val();
        $(this).html(
            `<div class="d-flex gap-1 align-items-center justify-content-center">
        <div> Log in</div>
        <div class="loader-small" />
      </div`
        );
        try {
            const user = await signIn({ username, password });
            window.location.href = "dashboard.html";
        } catch (error) {
            $(this).text("Log in");
            console.log(error);
            $("#root")
                .append(`<div id="customAlert" class=" alert custom-alert-danger">
                            <div class="flex-1">${error.message} </div>
                          </div>
                      `);
            setTimeout(function () {
                $("#customAlert").remove();
            }, 2000);
        }
    });

    $("#password-toggler").click(function () {
       togglePasswordVisibility("password", "password-toggler");
    });
    let auth = await getUserSession(false);
    if (auth.tokens) {
        window.location.href = "dashboard.html";
    }
});

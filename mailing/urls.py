from django.urls import path

from . import views

app_name = "mailing"

urlpatterns = [
    path("", views.MailingView.as_view(), name="home"),
    path("mail-receivers-list/", views.MailReceiverListView.as_view(), name="mail-receivers-list"),
    path("mail-receiver-detail/<int:pk>/", views.MailReceiverDetailView.as_view(), name="mail-receiver-detail"),
    path("mail-receiver-create/", views.MailReceiverCreateView.as_view(), name="mail-receiver-create"),
    path("mail-receiver-update/<int:pk>/", views.MailReceiverUpdateView.as_view(), name="mail-receiver-update"),
    path("mail-receiver-delete/<int:pk>/", views.MailReceiverDeleteView.as_view(), name="mail-receiver-delete"),
    path("messages-list/", views.MessageListView.as_view(), name="messages-list"),
    path("message-detail/<int:pk>/", views.MessageDetailView.as_view(), name="message-detail"),
    path("message-create/", views.MessageCreateView.as_view(), name="message-create"),
    path("message-update/<int:pk>/", views.MessageUpdateView.as_view(), name="message-update"),
    path("message-delete/<int:pk>/", views.MessageDeleteView.as_view(), name="message-delete"),
    path("mailing-unit-delete/<int:pk>/", views.MailingUnitDeleteView.as_view(), name="mailing-unit-delete"),
    path("mailing-units-list/", views.MailingUnitListView.as_view(), name="mailing-units-list"),
    path("mailing-unit-detail/<int:pk>/", views.MailingUnitDetailView.as_view(), name="mailing-unit-detail"),
    path("mailing-unit-create/", views.MailingUnitCreateView.as_view(), name="mailing-unit-create"),
    path("mailing-unit-update/<int:pk>/", views.MailingUnitUpdateView.as_view(), name="mailing-unit-update"),
    path("mailing-unit/send-mail/<int:pk>/", views.MailingUnitSendMailView.as_view(), name="mailing-unit-send-mail"),
    path(
        "mailing-unit/stop-mailing/<int:pk>/", views.MailingUnitStopMailView.as_view(), name="mailing-unit-stop-mail"
    ),
    path(
        "mailing-attempts-list/<int:mailing_id>", views.MailingAttemptListView.as_view(), name="mailing-attempts-list"
    ),
    path("all-mailing-attempts-list/", views.MailingAttemptListView.as_view(), name="all-mailing-attempts-list"),
    path("report/", views.ReportView.as_view(), name="report"),
]

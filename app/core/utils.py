from datetime import datetime

from app.models import Donation, CharityProject


def project_invest(
        project: CharityProject,
        donations: list[Donation]
):
    for donation in donations:
        if project.fully_invested:
            break

        founds = donation.full_amount - donation.invested_amount
        need_to_close = project.full_amount - project.invested_amount

        if founds > need_to_close:
            project.invested_amount = project.full_amount
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.invested_amount += need_to_close
        elif founds == need_to_close:
            project.invested_amount = project.full_amount
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.close_date = datetime.now()
        else:
            donation.fully_invested = True
            donation.invested_amount = donation.full_amount
            donation.close_date = datetime.now()
            project.invested_amount += founds

    return project


def donation_invest(
        donation: Donation,
        projects: list[CharityProject]
):
    for project in projects:
        if donation.fully_invested:
            break

        need_to_close = project.full_amount - project.invested_amount
        founds = donation.full_amount - donation.invested_amount

        if founds > need_to_close:
            project.invested_amount = project.full_amount
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.invested_amount += need_to_close

        elif founds == need_to_close:
            project.invested_amount = project.full_amount
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.close_date = datetime.now()
        else:
            donation.fully_invested = True
            donation.invested_amount = donation.full_amount
            donation.close_date = datetime.now()
            project.invested_amount += founds

        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True

    return donation

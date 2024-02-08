import datetime


class DatetimeHelper:
    @staticmethod
    def epoch_to_iso(epoch_time):
        try:
            # Convertir l'epoch en datetime
            dt_object = datetime.datetime.utcfromtimestamp(epoch_time)

            # Formater la date et l'heure au format ISO 8601
            iso_formatted = dt_object.strftime("%d/%m/%Y, %H:%M:%S")

            return iso_formatted
        except Exception as e:
            print(f"Erreur lors de la conversion de l'epoch en format ISO : {str(e)}")
            return None

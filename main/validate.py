from django.core.exceptions import ValidationError



def validate_file_size(file):
    max_file_size_in_mb = 1
    if file.size > max_file_size_in_mb * 1024 * 1024:
        raise ValidationError(f"Files cannot be larger than {max_file_size_in_mb}mb!")
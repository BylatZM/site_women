class FourDigitYearConverter:
  regex = "[0-9]{4}"

  def to_python(self, value):
    return int(value)
  
  def to_url(self, value):
    '''
    код преобразует число в строку
    % -  форматирование строки (сейчас используют str.format())
    4 - минимальное количество символов
    d - символы есть десятичные целые числа
    0 - ведущие нули (если длинна числа меньше 4 символов, то в начало подставятся нули)
    '''
    return "%04d" % value
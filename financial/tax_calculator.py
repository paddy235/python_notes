"""
由于现在个税计算方法比较复杂，网上的计算器又不够灵活，没有考虑涨工资、发奖金等情况，无法计算准确的扣税数据；
当然本脚本也非万能，只满足大部分用户需求。
本脚本默认配置：
    社保缴费：5825
    免征额度：5000
    专项扣除，用户第一次输入后，全年都按照此计算，不考虑中间有变化的场景
"""
try:
    special_deduction = int(input('请输入您专项扣除数，没有输入0：'))
except:
    print('您输入的数值有误！')

social_security = 5825
cumulative_wage = 0
last_wage = 0
cumulative_tax = 0
i = 1
while i < 13:

    if i == 1:
        try:
            last_wage = int(input('请输入您[%d]月的工资和奖金总数：' % i))
            cumulative_wage = last_wage
        except Exception as e:
            print('您输入的数值有误！')
    else:
        is_equal_choice = input('[%d]月的工资和奖金总数是否与上月相同？相同输入任意键，不相同输入"n"。' % i)
        if is_equal_choice == 'n':
            last_wage = int(input('请输入您[%d]月的工资和奖金总数：' % i))
        cumulative_wage = cumulative_wage + last_wage

    tax_base_num = cumulative_wage - 5000 * i - social_security * i - special_deduction * i

    tax_rate = 0.03 if tax_base_num < 36000 else (
                0.1 if tax_base_num < 144000 else (0.2 if tax_base_num < 300000 else (
                    0.25 if tax_base_num < 420000 else (
                        0.3 if tax_base_num < 660000 else (0.35 if tax_base_num < 960000 else 0.45)))))
    fastNum = 0 if tax_base_num < 36000 else (
                2520 if tax_base_num < 144000 else (16920 if tax_base_num < 300000 else (
                    31920 if tax_base_num < 420000 else (
                        52920 if tax_base_num < 660000 else (85920 if tax_base_num < 960000 else 181920)))))

    tax = tax_base_num * tax_rate - fastNum - cumulative_tax
    print('[%d]月税前工资: %d' % (i, last_wage))
    print('[%d]月五险一金: %d' % (i, social_security))
    print('[%d]月专项扣除: %d' % (i, special_deduction))
    print('[%d]月个税: %d' % (i, tax))
    print('[%d]月实发工资: %d' % (i, last_wage-social_security-tax))
    print('='*75)
    i += 1
    cumulative_tax += tax

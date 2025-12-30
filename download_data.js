const { getHistoricalRates } = require('dukascopy-node');
const { format, addMonths, startOfMonth, endOfMonth, isBefore, differenceInMonths } = require('date-fns');
const fs = require('fs').promises;
const path = require('path');
const cliProgress = require('cli-progress'); // اضافه کردن کتابخانه پروگرس‌بار

// --- تنظیمات طبق مستندات ارسالی شما ---
const config = {
    instruments: ['eurjpy', 'gbpjpy', 'gbpaud'],
    timeframes: ['m5', 'm15', 'h1', 'd1'],
    startDate: new Date('2023-01-01'),
    endDate: new Date('2023-12-31'),
    outputDir: './data_merged'
};

async function downloadAndMerge() {
    await fs.mkdir(config.outputDir, { recursive: true });

    // ۱. محاسبه تعداد کل تسک‌ها برای تنظیم پروگرس‌بار
    const totalMonths = differenceInMonths(config.endDate, config.startDate) + 1;
    const totalTasks = config.instruments.length * config.timeframes.length * totalMonths;

    // ۲. تعریف و شروع پروگرس‌بار
    const progressBar = new cliProgress.SingleBar({
        format: 'Downloading |' + '{bar}' + '| {percentage}% | {value}/{total} Months | Current: {info}',
        barCompleteChar: '\u2588',
        barIncompleteChar: '\u2591',
        hideCursor: true
    }, cliProgress.Presets.shades_classic);

    progressBar.start(totalTasks, 0, { info: 'Starting...' });

    for (const instrument of config.instruments) {
        for (const tf of config.timeframes) {
            let allData = [];
            let currentMonthStart = startOfMonth(config.startDate);

            while (isBefore(currentMonthStart, config.endDate)) {
                const fromDate = currentMonthStart;
                const toDate = endOfMonth(currentMonthStart);
                const monthStr = format(fromDate, 'yyyy-MM');
                
                // بروزرسانی وضعیت در پروگرس‌بار
                progressBar.update(progressBar.value, { 
                    info: `${instrument.toUpperCase()} ${tf} (${monthStr})` 
                });

                try {
                    // استفاده از ساختار getHistoricalRates طبق داکیومنت
                    const data = await getHistoricalRates({
                        instrument: instrument,
                        dates: {
                            from: fromDate,
                            to: toDate
                        },
                        timeframe: tf, // تغییر از interval به timeframe
                        format: 'json',
                        volumes: true,
                        ignoreFlats: true, // حذف روزهای تعطیل
                        useCache: true,    // استفاده از کش برای سرعت بیشتر
                        retryCount: 2      // تلاش مجدد در صورت خطا
                    });

                    if (data && data.length > 0) {
                        allData = allData.concat(data);
                    }
                } catch (error) {
                    // نمایش جزئیات خطا برای دیباگ بهتر
                    console.error(`   ❌ Error in ${format(fromDate, 'yyyy-MM')}:`, error.message || error);
                }

                progressBar.increment(); // رفتن به پله بعدی
                currentMonthStart = addMonths(currentMonthStart, 1);
            }

            // ذخیره فایل نهایی برای هر نماد/تایم‌فریم
            if (allData.length > 0) {
                allData.sort((a, b) => a.timestamp - b.timestamp);
                const fileName = `${instrument.toUpperCase()}-${tf}.json`;
                await fs.writeFile(path.join(config.outputDir, fileName), JSON.stringify(allData, null, 2));
            }
        }
    }

    progressBar.stop();
    console.log('\n✅ All downloads and merges completed successfully!');
}

downloadAndMerge().catch(console.error);
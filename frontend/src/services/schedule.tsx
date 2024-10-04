import axios from 'axios';

export interface Schedule {
    times: string[];
    days: Date[];
    n: number
}

export const sendSchedule = async (params: Schedule) => {
    console.log(params.times, params.days, params.n)
    try {
        const response = await axios.post('http://localhost:5000/api/schedule', params);
        console.log('Schedule sent successfully:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error sending schedule:', error);
        throw error;
    }
};
